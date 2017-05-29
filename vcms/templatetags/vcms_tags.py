# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import re
import time
from django import template
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType

from vcms.content.models import *
from vcms.share.models import *
from vcms.utils import encrypt

register = template.Library()
import logging as log


@register.inclusion_tag('vcms/comments/form.html', takes_context=True)
def vcms_comment(context, obj):
    d = ContentType.objects.get_for_model(obj)
    print(d.id)
    print(obj.pk)
    return {
        'obj': obj,
        'request': context['request'],
    }


@register.simple_tag(takes_context=True)
def old_ie_browser(context):
    is_old = False
    if 'HTTP_USER_AGENT' in context['request'].META:
        user_agent = context['request'].META['HTTP_USER_AGENT']
        pattern = "msie [1-8]\."
        prog = re.compile(pattern, re.IGNORECASE)
        match = prog.search(user_agent)

        if match:
            is_old = True

    return is_old


@register.simple_tag(takes_context=True)
def content_edit_link(context, obj):
    res = ''
    if context['request'].user.is_authenticated():
        if context['request'].user.is_superuser or obj.user == context['request'].user:
            res = '<a href="%s?page=%s">%s</a>' % (
                reverse('content_edit', args=[obj.type]),
                obj.hash,
                _(u'Edit content')
            )
    return mark_safe(res)


@register.inclusion_tag('vcms/admin.html', takes_context=True)
def vcms_admin(context):
    current_page_hash = None
    if 'content' in context:
        if hasattr(context['content'], 'url'):
            current_page_hash = context['content'].hash

    if context['request'].user.is_superuser is True:
        return {
            'menu': True,
            'current_page_hash': current_page_hash,
        }
    else:
        return {'menu': False}


@register.assignment_tag
def vcms_page(*args, **kwargs):
    url = kwargs.get('url')

    try:
        return Content.objects.filter(enabled=True, url=url).get()
    except Exception as e:
        log.error('Cannot get page by url: %s'% url)
        return None


@register.assignment_tag
def vcms_pages(*args, **kwargs):
    category = kwargs.get('category')
    parent = kwargs.get('parent')
    limit = kwargs.get('limit', 10)
    limit_from = kwargs.get('limit_from', 0)
    rs = Content.objects.filter(enabled=True)

    if parent:
        try:
            rs = rs.filter(url=parent).get().get_children()
        except:
            return []

    if category:
        rs = rs.filter(category__slug=category)

    rs = rs.filter(hidden=False).order_by('-date_published', '-id')
    return rs[limit_from:limit]


@register.assignment_tag()
def last_snippets(snippet_type='source', limit=20, show_hidden=False):
    res = Share.objects.filter(type=snippet_type, password='', disabled=False)
    if show_hidden is False:
        res = res.filter(hidden=False)
    res = res.order_by('-pk')[:limit]

    return {
        'records': res
    }


@register.simple_tag(takes_context=True)
def share_download_url(context, obj):
    remote_addr = context['request'].META['REMOTE_ADDR']
    timestamp = int(time.time())
    encrypted_key = encrypt(settings.SECRET_KEY[0:5], "%s %s" % (timestamp, remote_addr))
    return reverse('share_download_file', args=[obj.short_id, encrypted_key])


@register.simple_tag
def content_url(obj):
    if obj.type == 'gallery':
        return reverse('content_gallery', args=[obj.path])
    else:
        return reverse('content_page', args=[obj.url])


@register.simple_tag(takes_context=True)
def web_path(context, scheme='auto'):
    if scheme == 'auto':
        scheme = context['request'].scheme
    return "%s://%s" % (scheme, context['request'].get_host())


@register.simple_tag()
def content_get_snippet(name):
    rs = Snippet.objects.select_related().filter(slug=name)
    if rs:
        return mark_safe(rs[0].content)
    else:
        return None
