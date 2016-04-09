# -*- coding: utf-8 -*-
__author__ = 'Vadim'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'upload/', 'vcms.content.views.upload', name='jfu_upload'),
    url(r'^delete/(?P<pk>\d+)$', 'vcms.content.views.upload_delete', name='jfu_delete'),

    url(r'^index/(?P<content_type>[a-z]+)/$', 'vcms.content.views.index', name='content_index'),
    url(r'^index_personal/(?P<content_type>[a-z]+)/$', 'vcms.content.views.index_personal', name='content_index_personal'),
    url(r'^edit/(?P<content_type>[a-z]+)/$', 'vcms.content.views.add_or_edit', name='content_edit'),
    url(r'^post-(?P<path>[A-Za-z0-9/_-]+)/$', 'vcms.content.views.content_view', {'content_type': 'news'}, name='content_news'),
    url(r'^gallery-(?P<path>[A-Za-z0-9/_-]+)/$', 'vcms.content.views.content_view', {'content_type': 'gallery'}, name='content_gallery'),
    url(r'^(?P<path>[A-Za-z0-9/_-]+)/$', 'vcms.content.views.content_view', {'content_type': 'page'}, name='content_page'),
)
