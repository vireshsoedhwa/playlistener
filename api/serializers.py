from logging.config import valid_ident
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import URLValidator
from .models import MediaResource
from django.db import IntegrityError
import re
import magic
from .helper import create_hash
from django.core.files import File

import logging
logger = logging.getLogger(__name__)

class MediaResourceSerializer(serializers.ModelSerializer):
    audiofile = serializers.FileField(
        max_length=None, allow_empty_file=False, use_url=False)

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
        fields = ['id', 'title', 'genre', 'artists', 'tags', 
                  'audiofile', 'created_at']

    def create(self, validated_data):
        newaudio = MediaResource.objects.create()
        newaudio.save()
        newaudio.audiofile = validated_data.get(
            'audiofile', newaudio.audiofile)
        newaudio.md5_generated = validated_data.get(
            'md5_generated')
        newaudio.save()

        return newaudio
