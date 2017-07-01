# -*- coding: utf-8 -*-
__author__ = 'Vadim Kravciuk, vadim@kravciuk.com'

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import APIException

from vcms.utils import decrypt

from .models import Comment

import logging
log = logging.getLogger(__name__)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('approved', 'disabled')


class CommentPostSerializer(serializers.Serializer):
    comment = serializers.CharField()
    comment_for = serializers.CharField(max_length=200, write_only=True)
    comment_to = serializers.CharField(max_length=200, allow_blank=True, write_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):

        decoded = decrypt(settings.SECRET_KEY[:6], validated_data['comment_for'])
        if decoded is None:
            log.error('Failed decode string with object keys')
            raise APIException('Unknown source for comment')

        content_type_id, content_pk = decoded.decode('utf-8').split(':')

        x = Comment()
        x.comment = validated_data['comment']
        x.user = validated_data['user']
        x.content_type_id = int(content_type_id)
        x.content_pk = int(content_pk)
        try:
            x.save()
        except Exception as e:
            log.error(e)
            raise APIException('Error saving comment comment')
        return x