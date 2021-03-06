# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import os
import base64
from hashids import Hashids
from django.conf import settings
from vu.aes import AESCipher


def id_to_hash(short_id, salt=None, length=4):
    if salt is None:
        salt = settings.SECRET_KEY
    return Hashids(salt=salt, min_length=length).encrypt(short_id)


def hash_to_id(short_id, salt=None, length=4, default=0):
    if salt is None:
        salt = settings.SECRET_KEY
    hashids = Hashids(salt=salt, min_length=length)
    decrypt = hashids.decrypt(short_id)
    if len(decrypt) == 0:
        real_id = default
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


def unique_slug(instance, slug_field, slug, counter=0, query=None):
    if counter > 0:
        test_slug = "%s_%s" % (slug, counter)
    else:
        test_slug = slug

    rs = instance.objects.filter(**{slug_field: test_slug})
    if query:
        rs = rs.filter(**query)
    if rs[:1]:
        counter += 1
        return unique_slug(instance, slug_field, slug, counter, query)
    else:
        return test_slug


def encrypt(key, plaintext):
    aes = AESCipher(settings.SECRET_KEY[:16])
    x = aes.encrypt(plaintext).decode('utf-8')
    pad_count = x.count('=')
    return "%s%s" % (x.replace('=', ''), pad_count)


def decrypt(key, ciphertext):
    try:
        aes = AESCipher(settings.SECRET_KEY[:16])
        i = int(ciphertext[-1])
        ciphertext = "%s%s" % (ciphertext[:-1], '='*i)
        return aes.decrypt(ciphertext)
    except Exception as e:
        return e

