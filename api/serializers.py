from logging.config import valid_ident
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import MediaResource, Artist, Tag
from django.db import IntegrityError
import re
import magic
from .utils.hashlib import create_hash_from_file
from .utils.hashlib import create_hash_from_memory
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.core.files import File

import logging
logger = logging.getLogger(__name__)


class ArtistListingField(serializers.RelatedField):
    def to_representation(self, value):
        return f'{value.name}'

    def to_internal_value(self, data):
        return data

class MediaResourceSerializer(serializers.ModelSerializer):
    # artists = ArtistSerializer(many=True)
    audiofile = serializers.FileField(
        max_length=None, allow_empty_file=False, use_url=False)
    # artists = serializers.PrimaryKeyRelatedField(many=True, queryset=Artist.objects.all())
    artists = ArtistListingField(many=True, queryset=Artist.objects.all())

    def validate(self, attrs):
        tempaudiofile = attrs.get(
            'audiofile')
        file_type = None
        file_hash = None
        try:
            if(type(tempaudiofile) is InMemoryUploadedFile):
                file_type = magic.from_buffer(
                    tempaudiofile.read(2048), mime=True)
                file_hash = create_hash_from_memory(tempaudiofile)
            elif(type(tempaudiofile) is TemporaryUploadedFile):
                file_type = magic.from_file(
                    tempaudiofile.temporary_file_path(), mime=True)
                file_hash = create_hash_from_file(
                    tempaudiofile.temporary_file_path())
        except Exception as e:
            logger.error(e)
            raise serializers.ValidationError(
                tempaudiofile.name + " Could not be Validated")

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
        newrecord = MediaResource.objects.create()
        newrecord.save()
        newrecord.audiofile = validated_data.get(
            'audiofile', newrecord.audiofile)
        newrecord.md5_generated = validated_data.get(
            'md5_generated')

        artist_data = validated_data.get('artists')

        for artist in artist_data:
            print(artist)
            newrecord.artists.add(artist)
        # artists = Artist.objects.filter()
        # print(validated_data)
        # print(validated_data.get('artists'))
        # newrecord.save()
        # newrecord.artists.set(validated_data.get('artists'))
        return newrecord
