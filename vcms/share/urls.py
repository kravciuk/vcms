# -*- coding: utf-8 -*-
__author__ = 'Vadim'
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='share_index'),
    url(r'^personal/$', share_personal, name='share_personal'),
    url(r'^add/$', add_or_edit, name='share_add'),
    url(r'^edit/(?P<short_id>[A-Za-z0-9]+)/$', add_or_edit, name='share_edit'),
    url(r'^(?P<short_id>[A-Za-z0-9]+)/$', view_snippet, name='share_snippet'),
    url(r'^(?P<short_id>[A-Za-z0-9]+)/(?P<content_type>(raw))/$', view_snippet, name='share_raw_snippet'),
    url(r'^(?P<short_id>[A-Za-z0-9]+)/download/(?P<enc_key>[A-Za-z0-9]+)/$', download_file, name='share_download_file'),
    url(r'^(?P<short_id>[A-Za-z0-9]+)/link/$', link_redirect, name='share_link_redirect'),
]
