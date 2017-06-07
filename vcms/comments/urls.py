# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from .api import *

router = SimpleRouter()

router.register(r'comments', CommentViewSet)

urlpatterns = router.urls