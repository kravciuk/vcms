# -*- coding: utf-8 -*-
__author__ = 'Vadim'
from django.conf.urls import url
from .views import *


app_name = 'share'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^personal/$', share_personal, name='personal'),
    url(r'^add/$', add_or_edit, name='add'),
    url(r'^edit/(?P<short_id>[A-Za-z0-9]+)/$', add_or_edit, name='edit'),
    url(r'^(?P<short_id>[A-Za-z0-9]+)/$', view_snippet, name='snippet'),
    url(r'^(?P<short_id>[A-Za-z0-9]+)/forbidden/$', download_forbidden, name='download_forbidden'),
    url(r'^(?P<short_id>[A-Za-z0-9]+)/(?P<content_type>(raw))/$', view_snippet, name='raw_snippet'),
    url(r'^(?P<short_id>[A-Za-z0-9]+)/download/(?P<enc_key>[A-Za-z0-9_-]+)/$', download_file, name='download_file'),
    url(r'^(?P<short_id>[A-Za-z0-9]+)/link/$', link_redirect, name='link_redirect'),
]
