# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import os
from django.conf import settings
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import EmptyPage, PageNotAnInteger
from .forms import AddOrEditContentNews, PageContentForm
from .models import Content
from unidecode import unidecode
from flynsarmy_paginator.paginator import FlynsarmyPaginator
from jfu.http import upload_receive, UploadResponse, JFUResponse

import logging as log
# log = logging.getLogger(__name__)

@login_required
def index_personal(request, content_type="page"):
    return index(request, owner=True, content_type="page")


def index(request, owner=False, content_type="page"):
    full_listing = Content.objects.filter(hidden=False, enabled=True, type=content_type)
    if owner is True:
        full_listing = full_listing.filter(user=request.user)

    paginator = FlynsarmyPaginator(full_listing.order_by('-parent'), 30, adjacent_pages=20)
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
        instance = get_object_or_404(Content, url=page, user=request.user)
    else:
        instance = None

    if content_type is None or content_type == 'page':
        if request.method == 'POST':
            form = PageContentForm(request.POST, instance=instance)
            if form.is_valid():
                if form.cleaned_data.get('page'):
                    form.save()
                else:
                    after = form.cleaned_data.get('after')
                    if after:
                        node = get_object_or_404(Content, url=after, user=request.user)
                        new_node = node.add_child(user=request.user)
                    else:
                        new_node = Content.add_root(user=request.user)
                    form = PageContentForm(request.POST, instance=new_node)
                    instance = form.save(commit=False)
                    instance.user = request.user
                    instance.save()
            else:
                log.debug('Form error: %s' % form.errors)
        else:
            form = PageContentForm(instance=instance, initial={
                'after': after,
                'page': page,
            })
    elif content_type == 'news':
        if request.method == 'POST':
            form = AddOrEditContentNews(request.POST, instance=instance)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.type = Content.TYPE_NEWS
                instance.save()
            else:
                print 'FORM ERRROR'
                log.debug('Form error')
        else:
            form = AddOrEditContentNews(instance=instance)
    elif content_type == 'gallery':
        form = []

    return render(request, 'content/add_or_edit_%s.html' % content_type, {
        'form': form,

    })


def content_view(request, path, *args, **kwargs):
    instance = get_object_or_404(Content, enabled=True, url=path)
    return render(request, 'content/content_view.html', {
        'content': instance,
    })


@user_passes_test(lambda u: u.is_superuser)
@require_POST
def upload(request):

    # The assumption here is that jQuery File Upload
    # has been configured to send files one at a time.
    # If multiple files can be uploaded simulatenously,
    # 'file' may be a list of files.
    file_obj = upload_receive(request)

    filename = default_storage.get_valid_name(unidecode(file_obj.name))
    storage_name = default_storage.get_available_name(filename)
    default_storage.save(storage_name, file_obj)

    file_dict = {
        'name': default_storage.url(storage_name),
        'size': file_obj.size,

        'url': default_storage.url(storage_name),
        'thumbnailUrl': default_storage.url(storage_name),

        'deleteUrl': reverse('jfu_delete', kwargs={'pk': 1}),
        'deleteType': 'POST',
    }

    return UploadResponse(request, file_dict)


@user_passes_test(lambda u: u.is_superuser)
@require_POST
def upload_delete(request, pk):
    success = True
    # try:
    #     instance = YOURMODEL.objects.get( pk = pk )
    #     os.unlink( instance.file.path )
    #     instance.delete()
    # except YOURMODEL.DoesNotExist:
    #     success = False

    return JFUResponse(request, success)
