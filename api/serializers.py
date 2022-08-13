from logging.config import valid_ident
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import MediaResource
from django.db import IntegrityError
import re
import magic
from .utils.hashlib import create_hash_from_file
from .utils.hashlib import create_hash_from_memory
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.core.files import File

import logging
logger = logging.getLogger(__name__)


class MediaResourceSerializer(serializers.ModelSerializer):
    audiofile = serializers.FileField(
        max_length=None, allow_empty_file=False, use_url=False)

    def validate(self, attrs):
        tempaudiofile = attrs.get(
            'audiofile')
        file_type = None
        file_hash = None
        try:
            if(type(tempaudiofile) is InMemoryUploadedFile):
                file_type = magic.from_buffer(tempaudiofile.read(2048), mime=True)
                file_hash = create_hash_from_memory(tempaudiofile)
            elif(type(tempaudiofile) is TemporaryUploadedFile):
                file_type = magic.from_file(
                    tempaudiofile.temporary_file_path(), mime=True)
                file_hash = create_hash_from_file(
                    tempaudiofile.temporary_file_path())
        except Exception as e:
            logger.error(e)
            raise serializers.ValidationError(tempaudiofile.name + " Could not be Validated")

        if 'audio/mpeg' not in file_type:
            raise serializers.ValidationError(
                tempaudiofile.name + " is not a valid MP3 file")

        if MediaResource.objects.filter(md5_generated=file_hash).exists():
            raise serializers.ValidationError(
                tempaudiofile.name + " is already recorded")
        attrs['md5_generated'] = file_hash
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
