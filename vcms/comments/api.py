# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from .models import Comment
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets, mixins
from .serializer import CommentSerializer, CommentAdminSerializer, CommentPostSerializer


class CommentViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_class(self):
        if self.action in ('partial_update'):
            return CommentAdminSerializer
        else:
            return CommentSerializer
