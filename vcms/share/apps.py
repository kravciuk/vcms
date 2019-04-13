# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from django.apps import AppConfig


class DefaultConfig(AppConfig):
    name = 'share'

    def ready(self):
        from . import signals
