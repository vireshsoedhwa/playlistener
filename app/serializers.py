from logging.config import valid_ident
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import MediaResource, Artist, Tag, Genre
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

class GenreListingField(serializers.RelatedField):
    def to_representation(self, value):
        return f'{value.name}'

    def to_internal_value(self, data):
        return data


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
    artists = ArtistListingField(
        many=True, queryset=Artist.objects.all(), required=False)
    tags = TagListingField(
        many=True, queryset=Tag.objects.all(), required=False)
    genre = GenreListingField(
        many=False, queryset=Genre.objects.all(), required=False)
    title = serializers.CharField(
        max_length=500, min_length=None, allow_blank=True, required=False, trim_whitespace=True)

    def validate(self, attrs):
        logger.info("validate this ")
        tempaudiofile = attrs.get(
            'audiofile')
        if tempaudiofile is None:
            # raise serializers.ValidationError(
            #     "no files uploaded")
            return attrs
        file_type = None
        file_hash = None
        if (type(tempaudiofile) is InMemoryUploadedFile):
            file_type = magic.from_buffer(
                tempaudiofile.read(2048), mime=False)
            file_hash = create_hash_from_memory(tempaudiofile)
        elif (type(tempaudiofile) is TemporaryUploadedFile):
            file_type = magic.from_file(
                tempaudiofile.temporary_file_path(), mime=False)
            file_hash = create_hash_from_file(
                tempaudiofile.temporary_file_path())

        if 'Audio file' not in file_type:
            raise serializers.ValidationError(
                "not a valid audiofile")

        if MediaResource.objects.filter(md5_generated=file_hash).exists():
            raise serializers.ValidationError(
                "file already recorded")

        filename = re.sub(r".mp3$", "", tempaudiofile.name)
        attrs['md5_generated'] = file_hash
        attrs['title'] = filename
        return attrs

    def validate_artists(self, artist_list):
        print("validate artists")
        artist_list = [artist.lower() for artist in artist_list]
        return artist_list

    def validate_tags(self, tags_list):
        print("validate tags")
        tags_list = [tag.lower() for tag in tags_list]
        return tags_list

    def validate_genre(self, genre):
        print("validate genre")
        return genre.lower()

    def update(self, instance, validated_data):

        if "artists" in validated_data:
            artists = [Artist.objects.get_or_create(
                name=artist) for artist in validated_data.get('artists')]
            instance.artists.set([artist for artist, created in artists])

        if "tags" in validated_data:
            tags = [Tag.objects.get_or_create(
                name=tag) for tag in validated_data.get('tags')]
            instance.tags.set([tag for tag, created in tags])

        if "title" in validated_data:
            instance.title = validated_data.get('title')
            logger.info("Title updated")

        if "genre" in validated_data:
            genre, created = Genre.objects.get_or_create(
                name=validated_data.get('genre'))
            instance.genre = genre
            if created:
                logger.info(f"Genre updated: {genre}")
        return instance

    def create(self, validated_data):
        logger.info("create this ")
        newrecord = MediaResource.objects.create()
        newrecord.audiofile = validated_data.get(
            'audiofile')
        newrecord.md5_generated = validated_data.get(
            'md5_generated')
        if "artists" in validated_data:
            artists = [Artist.objects.get_or_create(
                name=artist) for artist in validated_data.get('artists')]
            newrecord.artists.set([artist for artist, created in artists])

        if "tags" in validated_data:
            tags = [Tag.objects.get_or_create(
                name=tag) for tag in validated_data.get('tags')]
            newrecord.tags.set([tag for tag, created in tags])

        if "title" in validated_data:
            newrecord.title = validated_data.get('title')
            logger.info("Title updated")

        if "genre" in validated_data:
            genre, created = Genre.objects.get_or_create(
                name=validated_data.get('genre'))
            newrecord.genre = genre
            if created:
                logger.info(f"New genre added: {genre}")
        newrecord.save()
        return newrecord

    class Meta:
        model = MediaResource
        # fields = '__all__'
        exclude = ['md5_generated']

