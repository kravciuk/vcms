# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from django.contrib import admin

from .models import Pygment
from .forms import AdminPygmentForm


@admin.register(Pygment)
class PygmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'enabled']
    list_filter = ['enabled']

    form = AdminPygmentForm
