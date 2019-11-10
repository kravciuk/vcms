# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import re
import time
from django.conf import settings
from django import template
from django.utils.translation import ugettext_lazy as _, get_language
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from vcms.content.models import *
from vcms.share.models import *
from vcms.comments.models import Comment
from vcms.utils import encrypt

register = template.Library()

from logging import getLogger
log = getLogger(__name__)


@register.simple_tag(takes_context=True)
def content_root_tree(context, show_hidden=False):
    rs = Content.objects.filter(enabled=True, depth=1, language=get_language()).order_by('path')
    if show_hidden is False:
        rs = rs.filter(hidden=False)
    return rs


@register.simple_tag(takes_context=True)
def content_annotate_list(context, show_hidden=False):
    rs = Content.get_annotated_list()
    if show_hidden is False:
        rs = rs.filter(hidden=False)
    return rs


@register.filter(name='addclass')
def addclass(field, my_class):
   return field.as_widget(attrs={"class":my_class})


@register.inclusion_tag('vcms/comments/form.html', takes_context=True)
def vcms_comment(context, obj):
    moderate_permission = False

    d = ContentType.objects.get_for_model(obj)
    rs = Comment.objects.filter(content_type=d, content_pk=obj.pk)
    if context['request'].user.is_superuser is False:
        rs = rs.filter(approved=True)

    if context['request'].user.is_superuser is True:
        moderate_permission = True

    return {
        'moderate_permission': moderate_permission,
        'records': rs,
        'obj': obj,
        'parent': encrypt(settings.SECRET_KEY, "%s:%s" % (d.pk, obj.pk)),
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


@register.simple_tag
def vcms_page(*args, **kwargs):
    url = kwargs.get('url')

    try:
        return Content.objects.filter(enabled=True, url=url).get()
    except Exception as e:
        log.error('Cannot get page by url: %s'% url)
        return None


@register.simple_tag(takes_context=True)
def vcms_pages(context, *args, **kwargs):
    category = kwargs.get('category')
    parent = kwargs.get('parent')
    language = kwargs.get('lang')
    limit = kwargs.get('limit', 10)
    page = context['request'].GET.get('page', 1)
    print(kwargs)

    rs = Content.objects.filter(enabled=True)
    if parent:
        try:
            rs = rs.filter(url=parent).get().get_children()
        except:
            return []

    if category:
        rs = rs.filter(category__slug=category)

    if language:
        rs = rs.filter(language=language)

    rs = rs.filter(hidden=False).order_by('-date_published', '-id')
    paginator = Paginator(rs, limit)

    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    return result


@register.simple_tag()
def last_snippets(snippet_type='source', limit=20, show_hidden=False):
    res = Share.objects.filter(type=snippet_type, password='', disabled=False, personal=False)
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
    encrypted_key = encrypt(settings.SECRET_KEY, "%s %s" % (timestamp, remote_addr))
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
