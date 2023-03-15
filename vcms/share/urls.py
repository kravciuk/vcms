# -*- coding: utf-8 -*-
__author__ = 'Vadim'
from django.urls import re_path
from .views import *


app_name = 'share'
urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^personal/$', share_personal, name='personal'),
    re_path(r'^add/$', add_or_edit, name='add'),
    re_path(r'^edit/(?P<short_id>[A-Za-z0-9]+)/$', add_or_edit, name='edit'),
    re_path(r'^(?P<short_id>[A-Za-z0-9]+)/$', view_snippet, name='snippet'),
    re_path(r'^(?P<short_id>[A-Za-z0-9]+)/forbidden/$', download_forbidden, name='download_forbidden'),
    re_path(r'^(?P<short_id>[A-Za-z0-9]+)/(?P<content_type>(raw))/$', view_snippet, name='source'),
    re_path(r'^(?P<short_id>[A-Za-z0-9]+)/download/(?P<enc_key>[A-Za-z0-9_-]+)/$', download_file, name='download'),
    re_path(r'^(?P<short_id>[A-Za-z0-9]+)/link/$', link_redirect, name='link_redirect'),
]
