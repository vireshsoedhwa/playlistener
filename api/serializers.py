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

import os

import logging
logger = logging.getLogger(__name__)

class TagListingField(serializers.RelatedField):
    def to_representation(self, value):
        return f'{value.name}'

    def to_internal_value(self, data):
        return data



class ArtistListingField(serializers.RelatedField):
    def to_representation(self, value):
        return f'{value.name}'

    def to_internal_value(self, data):
        return data


class MediaResourceSerializer(serializers.ModelSerializer):
    audiofile = serializers.FileField(
        max_length=None, allow_empty_file=False, use_url=False)
    artists = ArtistListingField(many=True, queryset=Artist.objects.all())
    tags = TagListingField(many=True, queryset=Tag.objects.all())
    title = serializers.CharField(
        max_length=500, min_length=None, allow_blank=True, required=False, trim_whitespace=True)
    description = serializers.CharField(
        max_length=5000, min_length=None, allow_blank=True, required=False, trim_whitespace=True)
    genre = serializers.CharField(
        max_length=100, min_length=None, allow_blank=True, required=False, trim_whitespace=True)
    def validate(self, attrs):
        tempaudiofile = attrs.get(
            'audiofile')
        if tempaudiofile is None:
            return attrs
        else:
            file_type = None
            file_hash = None
            try:
                if(type(tempaudiofile) is InMemoryUploadedFile):
                    file_type = magic.from_buffer(
                        tempaudiofile.read(2048), mime=False)
                    file_hash = create_hash_from_memory(tempaudiofile)
                elif(type(tempaudiofile) is TemporaryUploadedFile):
                    file_type = magic.from_file(
                        tempaudiofile.temporary_file_path(), mime=False)
                    file_hash = create_hash_from_file(
                        tempaudiofile.temporary_file_path())
            except Exception as e:
                logger.error(e)
                raise serializers.ValidationError(
                    tempaudiofile.name + " Could not be Validated")

            if 'Audio file' not in file_type:
                raise serializers.ValidationError(
                    tempaudiofile.name + " is not a valid MP3 file")

            if MediaResource.objects.filter(md5_generated=file_hash).exists():
                raise serializers.ValidationError(
                    tempaudiofile.name + " is already recorded")
            attrs['md5_generated'] = file_hash
            return attrs

    class Meta:
        model = MediaResource
        fields = ['id', 'title', 'description', 'genre', 'artists', 'tags',
                  'audiofile', 'created_at']

    def create(self, validated_data):
        newrecord = MediaResource.objects.create()
        newrecord.save()
        newrecord.audiofile = validated_data.get(
            'audiofile', newrecord.audiofile)
        newrecord.md5_generated = validated_data.get(
            'md5_generated')
        try:
            artist_data = validated_data.get('artists')
            for artist in artist_data:
                # first lookup if the artist exists if not then create it
                artistObject, created = Artist.objects.get_or_create(name=artist.lower())
                if created:
                    logger.info(f"New artist added: {artistObject}")
                newrecord.artists.add(artistObject)
        except:
            logger.info("Artists not updated")
        try:
            tag_data = validated_data.get('tags')
            for tag in tag_data:
                # first lookup if the tag exists if not then create it
                tagObject, created = Tag.objects.get_or_create(name=tag.lower())
                if created:
                    logger.info(f"New tag added: {tagObject}")
                newrecord.tags.add(tagObject)
        except:
            logger.info("Tags not updated")   
        newrecord.save()
        return newrecord

    def update(self, instance, validated_data):

        try:
            artist_data = validated_data.get('artists')
            for artist in artist_data:
                # first lookup if the artist exists if not then create it
                artistObject, created = Artist.objects.get_or_create(name=artist.lower())
                if created:
                    logger.info(f"New artist added: {artistObject}")
                instance.artists.add(artistObject)
        except:
            logger.info("Artists not updated")
    
        try:
            tag_data = validated_data.get('tags')
            for tag in tag_data:
                # first lookup if the tag exists if not then create it
                tagObject, created = Tag.objects.get_or_create(name=tag.lower())
                if created:
                    logger.info(f"New tag added: {tagObject}")
                instance.tags.add(tagObject)
        except:
            logger.info("Tags not updated")    
        
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.genre = validated_data.get('genre', instance.genre)
        return instance
