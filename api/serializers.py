from logging.config import valid_ident
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import URLValidator
from .models import MediaResource, YoutubeMediaResource
from django.db import IntegrityError
import re
import magic

import logging
logger = logging.getLogger(__name__)


class SubmitLinkSerializer(serializers.Serializer):

    youtube_id = serializers.CharField(
        #    validators=[validate_url],
        max_length=200,
        min_length=None,
        allow_blank=False)

    def create(self, validated_data):
        return YoutubeMediaResource.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.save()
        return instance


class GetfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(max_value=None, min_value=None)


# class YoutubeIdValidator:
#     def __init__(self):
#         pass

#     def __call__(self, value):
#         regExp = ".*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*"
#         x = re.search(regExp, value)
#     #     # http://img.youtube.com/vi/[video-id]/[thumbnail-number].jpg

#         if x == None:
#             raise serializers.ValidationError(
#                 f"[{value}] is not a valid youtube URL")
#         print(x.group(2))

#         # if value % self.base != 0:
#         #     message = 'This field must be a multiple of %d.' % self.base
#         #     raise serializers.ValidationError(message)


class YoutubeMediaResourceSerializer(serializers.ModelSerializer):

    youtube_id = serializers.CharField(
        max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)

    class Meta:
        model = YoutubeMediaResource
        fields = ['youtube_id', 'download_finished', 'busy',
                  'downloadprogress', 'eta', 'elapsed', 'speed']

    def create(self, validated_data):
        new_youtube_resource = YoutubeMediaResource.objects.create(
            **validated_data)
        new_youtube_resource.save()
        return new_youtube_resource

    def validate_youtube_id(self, value):
        regExp = ".*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*"
        x = re.search(regExp, value)
        # http://img.youtube.com/vi/[video-id]/[thumbnail-number].jpg
        if x == None:
            raise serializers.ValidationError(
                f"[{value}] is not a valid youtube URL")
    
        if YoutubeMediaResource.objects.filter(youtube_id = x.group(2)).exists():
            raise serializers.ValidationError(
                f"[{value}] has already been recorded")

        return x.group(2)


class MediaResourceSerializer(serializers.ModelSerializer):
    youtube_data = YoutubeMediaResourceSerializer(many=False, read_only=True)

    audiofile = serializers.FileField(
        max_length=None, allow_empty_file=False, use_url=False)
    # title = models.TextField(max_length=500, null=True, blank=True)
    # description = models.TextField(max_length=5000, null=True, blank=True)
    # genre = models.TextField(max_length=100, null=True, blank=True)
    # artist = models.TextField(max_length=100, null=True, blank=True)

    class Meta:
        model = MediaResource
        fields = ['id', 'title', 'genre',
                  'audiofile', 'youtube_data', 'created_at']

    def create(self, validated_data):
        newaudio = MediaResource.objects.create()
        newaudio.save()
        newaudio.audiofile = validated_data.get(
            'audiofile', newaudio.audiofile)
        newaudio.save()
        return newaudio

    def validate_audiofile(self, value):
        typeoffile = magic.from_file(value.temporary_file_path(), mime=True)
        if 'audio/mpeg' not in typeoffile:
            raise serializers.ValidationError(
                value.name + " is not a valid MP3")
        return value
