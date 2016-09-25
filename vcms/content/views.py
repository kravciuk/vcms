# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import os
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import EmptyPage, PageNotAnInteger
from .forms import PageContentForm
from .models import Content
from vcms.utils import id_to_hash, hash_to_id
from flynsarmy_paginator.paginator import FlynsarmyPaginator
# from jfu.http import upload_receive, UploadResponse, JFUResponse

import logging as log
# log = logging.getLogger(__name__)


def index(request, owner=False, content_type="page"):
    full_listing = Content.objects.filter(hidden=False, enabled=True, type=content_type)
    if owner is True:
        full_listing = full_listing.filter(user=request.user)

    paginator = FlynsarmyPaginator(full_listing.order_by('-id'), 30, adjacent_pages=20)
    page = request.GET.get('page')

    try:
        listing = paginator.page(page)
    except PageNotAnInteger:
        listing = paginator.page(1)
    except EmptyPage:
        listing = paginator.page(paginator.num_pages)

    content = []
    return render(request, 'content/index.html', {
        'content': content,
        'listing': listing,
        'host': request.META['HTTP_HOST'],
        'content_type': content_type,
    })


@login_required
def add_or_edit(request, content_type=None, parent=None):
    after = request.GET.get('after', request.POST.get('after'))
    page = request.GET.get('page', request.POST.get('page'))
    if page:
        instance = get_object_or_404(Content, id=hash_to_id(page, length=Content.HASH_LENGTH), user=request.user)
    else:
        instance = None

    if request.POST.get('delete_button') and instance is not None:
        try:
            ins_type = instance.type
            instance.delete()
            messages.add_message(request, messages.INFO, _(u'Record deleted.'))
            return redirect(reverse('content_index', args=[ins_type]))
        except Exception as e:
            messages.add_message(request, messages.ERROR, "%s %s" % (_(u'Failed to delete record.'), e))
            log.debug("Error deleting record: %s" % e)

    elif content_type is None or content_type == 'page':
        if request.method == 'POST' and request.POST.get('save_button'):
            form = PageContentForm(request.POST, instance=instance)
            if form.is_valid():
                if form.cleaned_data.get('page'):
                    instance = form.save()
                else:
                    after = form.cleaned_data.get('after')
                    if after:
                        node = get_object_or_404(Content, id=hash_to_id(after, length=Content.HASH_LENGTH), user=request.user)
                        new_node = node.add_child(user=request.user)
                    else:
                        new_node = Content.add_root(user=request.user)
                    form = PageContentForm(request.POST, instance=new_node)
                    instance = form.save(commit=False)
                    instance.user = request.user
                    instance.save()
                    form.save_m2m()
                messages.add_message(request, messages.INFO, _(u'Record saved.'))
                return redirect("%s?page=%s" % (reverse('content_edit', args=['page']), instance.hash))
            else:
                log.debug('Form error: %s' % form.errors)
        else:
            form = PageContentForm(instance=instance, initial={
                'after': after,
                'page': page,
            })
    elif content_type == 'gallery':
        form = []

    return render(request, 'content/add_or_edit_%s.html' % content_type, {
        'form': form,
        'instance': instance,
    })


def content_view(request, path, *args, **kwargs):
    instance = get_object_or_404(Content, enabled=True, url=path)
    return render(request, "content/%s.html" % instance.template, {
        'content': instance,
    })
