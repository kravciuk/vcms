# -*- coding: utf-8 -*-
__author__ = 'Vadim'

import os
import re
from datetime import datetime
from time import time
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseNotFound
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from imagekit import ImageSpec
from pilkit.processors import ResizeToFit
from vu.sendfile import sendfile

from .forms import AddSnippetForm
from .models import Share, SHARE_PROTECTED_DIR, SHARE_UPLOADED_DIR
from vcms.utils import hash_to_id, unique_file_name, encrypt, decrypt

from vu.paginator import FlynsarmyPaginator

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

import logging
log = logging.getLogger(__name__)


def download_forbidden(request, short_id):
    content = get_object_or_404(Share, slug=short_id, disabled=False)
    return render(request, 'share/download_forbiden.html', {
        'snippet': content,
    }, status=403)


def link_redirect(request, short_id):
    content = get_object_or_404(Share, slug=short_id, disabled=False)
    if content.url:
        return HttpResponsePermanentRedirect(content.url)
    else:
        return HttpResponseNotFound('Link not found.')


def download_file(request, short_id, enc_key):
    content = get_object_or_404(Share, slug=short_id, disabled=False)

    allow_download = True
    expiration_time = 0
    allowed_ip = '127.0.0.1'
    try:
        dec_string = decrypt(settings.SECRET_KEY, enc_key).split(' ')
        expiration_time = dec_string[0]
        allowed_ip = dec_string[1]

        if int(time()) > int(expiration_time) + settings.VCMS_DOWNLOAD_TIME_LIMIT:
            allow_download = False
            log.error("%s for object %s download - time expired." % (request.META['REMOTE_ADDR'], short_id))

        if allowed_ip != request.META['REMOTE_ADDR']:
            allow_download = False
            log.error("%s for object %s download - IP failed, accepted %s." % (request.META['REMOTE_ADDR'], short_id, allowed_ip))
    except Exception as e:
        log.debug(e, exc_info=True)
        allow_download = False
        log.error("%s for object %s download - failed decode string." % (request.META['REMOTE_ADDR'], short_id))

    if content.file and allow_download is True:
        file_path = os.path.join(settings.MEDIA_ROOT, content.file.name)
        return sendfile(
            request,
            file_path,
            attachment=True,
            attachment_filename=content.file_name
        )
    else:
        return redirect('share_download_forbidden', short_id=short_id)


def view_snippet(request, short_id, content_type='html'):
    content = get_object_or_404(Share, slug=short_id, disabled=False)
    if content_type == 'raw':
        replace = re.compile(r'(\r\n|\r|\r)')
        return HttpResponse(replace.sub('\n', content.content), content_type='text/plain')
    else:
        return render(request, 'share/snippet.html', {
            'snippet': content,
        })


@login_required
def add_or_edit(request, short_id=''):
    old_id = hash_to_id(short_id, default=0)

    res = Share.objects.filter(pk=old_id, user=request.user)[:1]
    if res:
        instance = res[0]
    else:
        instance = None
    form = AddSnippetForm(instance=instance)

    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('delete') and instance is not None:
            instance.delete()
            return redirect('share_personal')

        form = AddSnippetForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = request.user

            # format content
            if instance.content != '':
                lexer = get_lexer_by_name(instance.type, stripall=True)
                formatter = HtmlFormatter(linenos=True, cssclass="codehilite")
                instance.content_html = highlight(instance.content, lexer, formatter)
            else:
                instance.content_html = None

            if request.FILES.get('file'):
                if instance.pk:
                    instance.thumbnail = None
                    instance.rm_files()

                result = _upload_file(request.FILES['file'], password=instance.password)
                file_full_path = os.path.join(result.raw_path, result.name)
                instance.file_name = request.FILES['file'].name[:128]
                instance.file = os.path.join(result.path, result.name)

                if instance.file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    source = open(file_full_path, 'rb')
                    try:
                        th = Thumbnail(source=source)
                        th_content = th.generate()
                        fp = open(os.path.join(result.raw_path, 'th_'+result.name), 'wb')
                        fp.write(th_content.read())
                        fp.close()
                        source.close()
                        th_content.close()
                        instance.thumbnail = os.path.join(result.path, 'th_'+result.name)
                    except Exception as e:
                        log.error("Error creating thumbnail file: %s" % e)

            instance.save()
            form.save_m2m()
            return redirect('share_snippet', short_id=instance.short_id)

    return render(request, 'share/form.html', {
        'form': form,
        'instance': instance,
    })


def _upload_file(file_object, password=None):
    filename, file_extension = os.path.splitext(file_object.name)
    file_name = "%s%s" % (slugify(filename), file_extension)
    upload_path = os.path.join(settings.MEDIA_ROOT, SHARE_UPLOADED_DIR)
    access_path = SHARE_UPLOADED_DIR

    if password != '':
        upload_path = os.path.join(upload_path, SHARE_PROTECTED_DIR)
        access_path = os.path.join(access_path, SHARE_PROTECTED_DIR)

    today = datetime.date(datetime.now())
    upload_path = os.path.join(upload_path, "%s/%s/%s" % (today.strftime("%y"), today.month, today.day))
    access_path = os.path.join(access_path, "%s/%s/%s" % (today.strftime("%y"), today.month, today.day))

    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    new_file_name = unique_file_name(upload_path, file_name)
    fp = open('%s/%s' % (upload_path, new_file_name), 'wb')
    for chunk in file_object.chunks():
        fp.write(chunk)
    fp.close()

    result = lambda: result
    result.path = access_path
    result.raw_path = upload_path
    result.name = new_file_name

    return result


@login_required
def share_personal(request):
    return index(request, owner=True)


def index(request, owner=False):
    share_list = Share.objects.filter(hidden=False, disabled=False)
    if owner is True:
        share_list = share_list.filter(user=request.user)

    paginator = FlynsarmyPaginator(share_list.order_by('-id'), 30, adjacent_pages=20)
    page = request.GET.get('page')

    try:
        shares = paginator.page(page)
    except PageNotAnInteger:
        shares = paginator.page(1)
    except EmptyPage:
        shares = paginator.page(paginator.num_pages)

    content = []
    return render(request, 'share/index.html', {'content': content,
                                                'shares': shares,
                                                'host': request.META['HTTP_HOST']})


class Thumbnail(ImageSpec):
    processors = [ResizeToFit(settings.VCMS_SHARE_THUMBNAIL_WEIGHT, settings.VCMS_SHARE_THUMBNAIL_HEIGHT, False)]
    format = 'JPEG'
    options = {'quality': 80}
