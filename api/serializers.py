from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import URLValidator
from .models import MediaResource, YoutubeMediaResource
from django.db import IntegrityError
import re

from django_q.tasks import async_task, result, fetch

import logging
logger = logging.getLogger(__name__)


# def validate_url(value):
#     regExp = ".*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*"
#     x = re.search(regExp, value)
# http://img.youtube.com/vi/[video-id]/[thumbnail-number].jpg

#     if x == None:
#         raise serializers.ValidationError("Not a Valid youtube URL: " + value)


class SubmitLinkSerializer(serializers.Serializer):

    youtube_id = serializers.CharField(
        #    validators=[validate_url],
        max_length=200,
        min_length=None,
        allow_blank=False)
    # title = serializers.CharField(
    #     max_length=500,
    #     min_length=None,
    #     allow_blank=True)
    # genre = serializers.CharField(
    #     max_length=100,
    #     min_length=None,
    #     allow_blank=True)

    def create(self, validated_data):
        print("creationnn")
        return YoutubeMediaResource.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # instance.url = validated_data.get('url', instance.url)
        # instance.save()
        # instance.youtube_id = validated_data.get(
        #     'youtube_id', instance.youtube_id)
        # instance.title = validated_data.get('title', instance.title)
        # instance.genre = validated_data.get('genre', instance.genre)
        print("updatinnnggg")
        instance.save()
        return instance


class GetfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(max_value=None, min_value=None)


class ListRequestSerializer(serializers.Serializer):
    count = serializers.IntegerField(max_value=None, min_value=None)


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaResource
        fields = ['id', 'youtube_id', 'title', 'genre',
                  'download_finished', 'busy', 'created_at']
