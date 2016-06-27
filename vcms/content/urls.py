# -*- coding: utf-8 -*-
__author__ = 'Vadim'
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^index/(?P<content_type>[a-z]+)/$', index, name='content_index'),
    url(r'^edit/(?P<content_type>[a-z]+)/$', add_or_edit, name='content_edit'),
    url(r'^post-(?P<path>[A-Za-z0-9/_-]+)/$', content_view, {'content_type': 'news'}, name='content_news'),
    url(r'^gallery-(?P<path>[A-Za-z0-9/_-]+)/$', content_view, {'content_type': 'gallery'}, name='content_gallery'),
    url(r'^(?P<path>[A-Za-z0-9/_-]+)/$', content_view, kwargs={'content_type': 'page'}, name='content_page'),
]
