# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import re
import time
from django.conf import settings
from django import template
from django.utils.translation import gettext_lazy as _, get_language
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from vcms.share.models import Share

register = template.Library()

from logging import getLogger
log = getLogger(__name__)


@register.simple_tag(takes_context=True)
def list_snipets(context, **kwargs):
    tags = kwargs.get('tags')
    limit = kwargs.get('limit', 10)
    page = context['request'].GET.get('page', 1)

    rs = Share.objects.filter(hidden=False, password='', disabled=False, personal=True).order_by('-time_updated')

    paginator = Paginator(rs, limit)

    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    return result


@register.simple_tag(takes_context=True)
def show_snipets(context, **kwargs):
    return Share.objects.filter(slug=context['slug']).first()
