# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk'

import os
from hashids import Hashids
from django.conf import settings


def hash_to_id(short_id, default=None):
    hashids = Hashids(salt=settings.SECRET_KEY, min_length=4)
    decrypt = hashids.decrypt(short_id)
    if len(decrypt) == 0:
        real_id = None
    else:
        real_id = decrypt[0]

    return real_id


def unique_file_name(dir_path, file_name):
    if not os.path.exists("%s/%s" % (dir_path, file_name)):
        return file_name
    else:
        _file, _ext = os.path.splitext(file_name)
        i = 1
        while os.path.exists("%s/%s_%s%s" % (dir_path, _file, str(i), _ext)):
            i += 1
        return "%s_%s%s" % (_file, str(i), _ext)
