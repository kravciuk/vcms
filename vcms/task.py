# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from .content.models import Content
from .content.rehost import Rehost

from logging import getLogger
log = getLogger(__name__)

def rehost_content(pk):
    log.debug("Rehost started")
    obj = Content.objects.get(pk=pk)
    html = Rehost.images(obj.content)
    obj.content = html
    obj.save()
