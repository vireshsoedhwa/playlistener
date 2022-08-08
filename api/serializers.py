from logging.config import valid_ident
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import URLValidator
from .models import MediaResource, YoutubeMediaResource
from django.db import IntegrityError
import re
import magic
from .helper import create_hash
from django.core.files import File

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


class YoutubeMediaResourceSerializer(serializers.ModelSerializer):

    youtube_id = serializers.CharField(
        max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)

    class Meta:
        model = YoutubeMediaResource
        fields = ['youtube_id', 'status', 'downloadprogress',
                  'eta', 'elapsed', 'speed']

    def create(self, validated_data):

        if YoutubeMediaResource.objects.filter(youtube_id=validated_data['youtube_id']).exists():
            existing_youtube_resource = YoutubeMediaResource.objects.get(
                youtube_id=validated_data['youtube_id'])
            return existing_youtube_resource

        new_youtube_resource = YoutubeMediaResource.objects.create(
            **validated_data)
        return new_youtube_resource

    def validate_youtube_id(self, value):
        regExp = ".*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*"
        x = re.search(regExp, value)
        # http://img.youtube.com/vi/[video-id]/[thumbnail-number].jpg
        if x == None:
            raise serializers.ValidationError(
                f"[{value}] is not a valid youtube URL")

        return x.group(2)


class MediaResourceSerializer(serializers.ModelSerializer):
    youtubedata = YoutubeMediaResourceSerializer(many=False, read_only=True)

    audiofile = serializers.FileField(
        max_length=None, allow_empty_file=False, use_url=False)
    # title = serializers.CharField(
    #     max_length=500,
    #     min_length=None,
    #     allow_blank=True)

    # description = models.TextField(max_length=5000, null=True, blank=True)
    # genre = models.TextField(max_length=100, null=True, blank=True)
    # artist = models.TextField(max_length=100, null=True, blank=True)

    def validate(self, attrs):
        tempaudiofile_object = attrs.get(
            'audiofile')
        typeoffile = magic.from_file(
            tempaudiofile_object.temporary_file_path(), mime=True)
        if 'audio/mpeg' not in typeoffile:
            raise serializers.ValidationError(
                tempaudiofile_object.name + " is not a valid MP3")

        md5 = create_hash(tempaudiofile_object.temporary_file_path())
        if MediaResource.objects.filter(md5_generated=md5).exists():
            raise serializers.ValidationError(
                tempaudiofile_object.name + " is already recorded")
        attrs['md5_generated'] = md5
        return attrs

    class Meta:
        model = MediaResource
        fields = ['id', 'title', 'genre',
                  'audiofile', 'youtubedata', 'created_at']

    def create(self, validated_data):
        newaudio = MediaResource.objects.create()
        newaudio.save()
        newaudio.audiofile = validated_data.get(
            'audiofile', newaudio.audiofile)
        newaudio.md5_generated = validated_data.get(
            'md5_generated')
        newaudio.save()

        return newaudio
