# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import pathlib
from datetime import date

from django.conf import settings
from vu.image import VuImage

from vcms.share.models import Share, File

TH_SIZE = settings.VCMS_SHARE_TH_SIZE if hasattr(settings, 'VCMS_SHARE_TH_SIZE') else (260, 260)

def share_cleaner():
    Share.objects.filter(time_delete__lte=date.today(), time_delete__isnull=False).delete()


def task_share_process_file(pk):
    obj = File.objects.get(id=pk)
    if obj.mime in [File.TYPE_IMAGE]:
        VuImage.normalize_orientation(obj.file.path)

        extension = pathlib.Path(obj.file.path).suffix
        th_name = obj.file.path.replace(extension, f'_th{extension}')
        VuImage.resize(obj.file.path, target=th_name, maxsize=TH_SIZE)
    return