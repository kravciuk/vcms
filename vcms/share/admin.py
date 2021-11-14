# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from django.contrib import admin

from .models import Pygment


@admin.register(Pygment)
class PygmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'enabled']
    list_filter = ['enabled']
