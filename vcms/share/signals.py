# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

import os
import logging
import mimetypes

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from django.conf import settings
from django.utils.text import Truncator
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import Share, File

log = logging.getLogger(__name__)


@receiver([post_save,], dispatch_uid="signal_share_post_save", sender=Share)
def process_snippet(sender, instance=None, created=False, **kwargs):
    log.debug("Updating instance by signal")

    if instance.content and instance.type:
        lexer = get_lexer_by_name(instance.type.code, stripall=True)
        formatter = HtmlFormatter(linenos=True, cssclass="codehilite")
        instance.json['html'] = highlight(instance.content, lexer, formatter)
    elif instance.content:
        instance.json['html'] = '<br />\n'.join(instance.content.split('\n'))
    else:
        instance.json['html'] = None

    if not instance.title and instance.description:
        instance.title = Truncator(Truncator(instance.description).chars(255)).words(15)

    Share.objects.filter(id=instance.id).update(
        json=instance.json,
        title = instance.title,
    )


@receiver([post_delete], dispatch_uid='signal_share_post_delete', sender=Share)
def share_on_delete(sender, instance, **kwargs):
    instance.tags.clear()


@receiver([post_save,], dispatch_uid="signal_share_file_post_save", sender=File)
def signal_share_file_post_save(sender, instance=None, created=False, **kwargs):
    mime_type = mimetypes.guess_extension(instance.file.path)
    log.debug(mime_type)
    # File.objects.filter(id=instance.id).update(
    #     mime=mime_type[0]
    # )

@receiver([post_delete,], dispatch_uid="signal_share_file_post_delete", sender=File)
def signal_share_file_post_delete(sender, instance=None, created=False, **kwargs):
    def rm_dir(path, count):
        if count > 3:
            return
        if os.listdir(path) == 0:
            os.remove(path)
        return rm_dir(os.path.dirname(path), (count+1))

    log.debug("Removing %s" % instance.file.path)
    os.remove(instance.file.path)

    rm_dir(os.path.dirname(instance.file.path), 1)
