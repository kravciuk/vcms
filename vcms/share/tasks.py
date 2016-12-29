# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from vcms.share.models import Share
from datetime import date


def share_cleaner():
    Share.objects.filter(time_delete__lte=date.today(), time_delete__isnull=False).delete()
