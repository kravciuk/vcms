# -*- coding: utf-8 -*-
__author__ = 'Vadim'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'vcms.share.views.index', name='share_index'),
    url(r'^personal/$', 'vcms.share.views.share_personal', name='share_personal'),
    url(r'^add/$', 'vcms.share.views.add_or_edit', name='share_add'),
    url(r'^edit/(?P<short_id>[A-Za-z0-9]+)/$', 'vcms.share.views.add_or_edit', name='share_edit'),
    url(r'^(?P<short_id>[A-Za-z0-9]+)/$', 'vcms.share.views.view_snippet', name='share_snippet'),
    url(r'^(?P<short_id>[A-Za-z0-9]+)/(?P<content_type>(raw))/$', 'vcms.share.views.view_snippet', name='share_raw_snippet'),
    url(r'^(?P<short_id>[A-Za-z0-9]+)/download/$', 'vcms.share.views.download_file', name='share_download_file'),
    url(r'^(?P<short_id>[A-Za-z0-9]+)/link/$', 'vcms.share.views.link_redirect', name='share_link_redirect'),
)
