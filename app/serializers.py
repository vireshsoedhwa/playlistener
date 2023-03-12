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


class MediaResourceListSerializer(serializers.Serializer):
    audiofile = serializers.ListField(
        child=serializers.FileField(
            max_length=None, allow_empty_file=False, use_url=False)
    )

    def validate(self, attrs):
        logger.info("validate this ")
        # logger.info(attrs)
        tempaudiofile = attrs.get(
            'audiofile')
        if tempaudiofile is None:
            raise serializers.ValidationError(
                "no files uploaded")

        valid_files = []
        invalid_files = []
        already_recorded = []
        for index, item in enumerate(tempaudiofile):
            print(index)
            print(type(item))
            file_type = None
            file_hash = None
            try:
                if (type(item) is InMemoryUploadedFile):
                    file_type = magic.from_buffer(
                        item.read(2048), mime=False)
                    file_hash = create_hash_from_memory(item)
                elif (type(item) is TemporaryUploadedFile):
                    file_type = magic.from_file(
                        item.temporary_file_path(), mime=False)
                    file_hash = create_hash_from_file(
                        item.temporary_file_path())
            except Exception as e:
                logger.error(e)
                invalid_files.append(item)
                continue

            # print(file_type)
            # check mimetype
            if 'Audio file' not in file_type:
                print(f"{index} not an audio file")
                print(file_type)
                invalid_files.append(item)
                continue

            try:
                # check if this file already exists
                if MediaResource.objects.filter(md5_generated=file_hash).exists():
                    print(f"{index} hash already exists")
                    already_recorded.append(item)
                    continue
            except:
                print(f"{index} failed to check hash")
                already_recorded.append(item)
                continue
            valid_files.append([item, file_hash])

        attrs['valid'] = valid_files
        attrs['invalid'] = invalid_files
        attrs['already_recorded'] = already_recorded
        return attrs


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
    def validate(self, attrs):
        logger.info("validate this ")
        tempaudiofile = attrs.get(
            'audiofile')
        if tempaudiofile is None:
            raise serializers.ValidationError(
                "no files uploaded")
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

    class Meta:
        model = MediaResource
        fields = '__all__'


'''
# class TagListingField(serializers.RelatedField):
#     def to_representation(self, value):
#         return f'{value.name}'

#     def to_internal_value(self, data):
#         return data


# class ArtistListingField(serializers.RelatedField):
#     def to_representation(self, value):
#         return f'{value.name}'

#     def to_internal_value(self, data):
#         return data


class MediaResourceSerializer(serializers.ModelSerializer):
    # audiofiles = serializers.ListField(
    #     child=serializers.FileField(max_length=None,
    #                                 allow_empty_file=False,
    #                                 use_url=False)
    # )
    file = serializers.FileField(
        max_length=None, allow_empty_file=False, use_url=False)
    # artists = ArtistListingField(many=True, queryset=Artist.objects.all())
    # tags = TagListingField(many=True, queryset=Tag.objects.all())
    # title = serializers.CharField(
    #     max_length=500, min_length=None, allow_blank=True, required=False, trim_whitespace=True)
    # description = serializers.CharField(
    #     max_length=5000, min_length=None, allow_blank=True, required=False, trim_whitespace=True)
    # genre = serializers.CharField(
    #     max_length=100, min_length=None, allow_blank=True, required=False, trim_whitespace=True)

    def validate(self, attrs):

        logger.info("validate this ")

        # tempaudiofile = attrs.get(
        #     'audiofile')
        # if tempaudiofile is None:
        #     return attrs
        # else:
        #     file_type = None
        #     file_hash = None
        #     try:
        #         if(type(tempaudiofile) is InMemoryUploadedFile):
        #             file_type = magic.from_buffer(
        #                 tempaudiofile.read(2048), mime=False)
        #             file_hash = create_hash_from_memory(tempaudiofile)
        #         elif(type(tempaudiofile) is TemporaryUploadedFile):
        #             file_type = magic.from_file(
        #                 tempaudiofile.temporary_file_path(), mime=False)
        #             file_hash = create_hash_from_file(
        #                 tempaudiofile.temporary_file_path())
        #     except Exception as e:
        #         logger.error(e)
        #         raise serializers.ValidationError(
        #             tempaudiofile.name + " Could not be Validated")

        #     if 'Audio file' not in file_type:
        #         raise serializers.ValidationError(
        #             tempaudiofile.name + " is not a valid MP3 file")

        #     if MediaResource.objects.filter(md5_generated=file_hash).exists():
        #         raise serializers.ValidationError(
        #             tempaudiofile.name + " is already recorded")
        #     attrs['md5_generated'] = file_hash

        #     if attrs.get('title') is None:
        #         # get title from audio file
        #         filename = re.sub(r".mp3$", "", tempaudiofile.name)
        #         attrs['title'] = filename
        return attrs

    class Meta:
        model = MediaResource
        fields = ['file']


    def create(self, validated_data):

        print("creating new record")
        return None


    def create(self, validated_data):
        logger.info("create this ")
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
                if len(artist) > 1:
                    artistObject, created = Artist.objects.get_or_create(
                        name=artist.lower())
                    if created:
                        logger.info(f"New artist added: {artistObject}")
                    newrecord.artists.add(artistObject)
        except:
            logger.info("Artists not updated")
        try:
            tag_data = validated_data.get('tags')
            for tag in tag_data:
                # first lookup if the tag exists if not then create it
                tagObject, created = Tag.objects.get_or_create(
                    name=tag.lower())
                if created:
                    logger.info(f"New tag added: {tagObject}")
                newrecord.tags.add(tagObject)
        except:
            logger.info("Tags not updated")

        try:
            newrecord.title = validated_data.get('title')
        except:
            logger.info("title not included")

        try:
            newrecord.description = validated_data.get('description')
        except:
            logger.info("description not included")

        try:
            newrecord.genre = validated_data.get('genre')
        except:
            logger.info("genre not included")

        newrecord.save()
        return newrecord

    def update(self, instance, validated_data):
        logger.info("update this ")
        try:
            artist_data = validated_data.get('artists')
            for artist in artist_data:
                # first lookup if the artist exists if not then create it
                if len(artist) > 1:
                    artistObject, created = Artist.objects.get_or_create(
                        name=artist.lower())
                    if created:
                        logger.info(f"New artist added: {artistObject}")
                    instance.artists.add(artistObject)
        except:
            logger.info("Artists not updated")

        try:
            tag_data = validated_data.get('tags')
            for tag in tag_data:
                # first lookup if the tag exists if not then create it
                tagObject, created = Tag.objects.get_or_create(
                    name=tag.lower())
                if created:
                    logger.info(f"New tag added: {tagObject}")
                instance.tags.add(tagObject)
        except:
            logger.info("Tags not updated")

        try:
            instance.title = validated_data.get('title', instance.title)
        except:
            logger.info("title not updated")

        try:
            instance.description = validated_data.get(
                'description', instance.description)
        except:
            logger.info("descripton not updated")

        try:
            instance.genre = validated_data.get('genre', instance.genre)
        except:
            logger.info("genre not updated")

        return instance
'''
