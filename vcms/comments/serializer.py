# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Comment


class CommentSerializer(serializers.Serializer):
    comment = serializers.CharField(max_length=200)
    parent = serializers.CharField(max_length=200)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('user', 'content_type', 'content_pk', 'comment')

    def create(self, validated_data):
        x = Comment()
        x.comment = validated_data['comment']
        x.user = validated_data['user']
        x.save()
        return x