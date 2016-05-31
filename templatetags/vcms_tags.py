# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from vcms.content.models import *
from vcms.share.models import *

register = template.Library()
import logging as log


@register.simple_tag(takes_context=True)
def content_edit_link(context, obj):
    if context['request'].user.is_authenticated():
        if context['request'].user.is_superuser or obj.user == context['request'].user:
            return '<a href="%s?page=%s">%s</a>' % (
                reverse('content_edit', args=[obj.type]),
                obj.url,
                _(u'Edit content')
            )
    return ''



@register.inclusion_tag('vcms/admin.html', takes_context=True)
def vcms_admin(context):
    current_page_url = None
    if 'content' in context:
        if hasattr(context['content'], 'url'):
            current_page_url = context['content'].url

    if context['request'].user.is_superuser is True:
        return {
            'menu': True,
            'current_page_url': current_page_url,
        }
    else:
        return {'menu': False}


@register.assignment_tag
def vcms_page(*args, **kwargs):
    url = kwargs.get('url')

    try:
        return Content.objects.filter(enabled=True, url=url).get()
    except Exception as e:
        log.error('Cannot get page by url: '% url)
        return ''

@register.assignment_tag
def vcms_pages(*args, **kwargs):
    category = kwargs.get('category')
    parent = kwargs.get('parent')
    limit = kwargs.get('limit', 10)
    limit_from = kwargs.get('limit_from', 0)

    rs = Content.objects.filter(enabled=True, hidden=False)
    # if parent:
    #     rs = rs.filter(parent__path=parent)
    # else:
    #     rs = rs.filter(parent=None)
    if category:
        rs = rs.filter(category__slug=category)
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


@register.simple_tag
def content_url(obj):
    if obj.type == 'gallery':
        return reverse('content_gallery', args=[obj.path])
    elif obj.type == 'news':
        return reverse('content_news', args=[obj.path])
    else:
        return reverse('content_page', args=[obj.path])


@register.simple_tag(takes_context=True)
def web_path(context, scheme='auto'):
    if scheme == 'auto':
        scheme = context['request'].scheme
    return "%s://%s" % (scheme, context['request'].get_host())


@register.assignment_tag
def content_get_snippet(request, name):
    rs = Snippet.objects.select_related().filter(slug=name)
    if rs:
        return rs[0]
    else:
        return None
