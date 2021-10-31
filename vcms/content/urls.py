# -*- coding: utf-8 -*-
__author__ = 'Vadim'
from django.conf.urls import url
from .views import *

app_name = 'content'
urlpatterns = [
    url(r'^index/(?P<content_type>[a-z]+)/$', index, name='index'),
    url(r'^edit/(?P<content_type>[a-z]+)/$', add_or_edit, name='edit'),
    url(r'^post-(?P<path>[A-Za-z0-9/_-]+)/$', content_view, {'content_type': 'news'}, name='news'),
    url(r'^gallery-(?P<path>[A-Za-z0-9/_-]+)/$', content_view, {'content_type': 'gallery'}, name='gallery'),
    url(r'^(?P<path>[A-Za-z0-9/_-]+)/$', content_view, kwargs={'content_type': 'page'}, name='page'),
    url(r'^$', content_view, kwargs={'content_type': 'page'}, name='page_index'),
]
