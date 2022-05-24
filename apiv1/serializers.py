from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import URLValidator
from .models import Resource
from django.db import IntegrityError
import re

from django_q.tasks import async_task, result, fetch


class ResourceSerializer(serializers.Serializer):

    # id = serializers.CharField(max_length=None, min_length=None, allow_blank=True, trim_whitespace=True)
    url = serializers.URLField(validators=[URLValidator], max_length=200, min_length=None, allow_blank=True)
    # urlid = serializers.SlugField(max_length=200, allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = Resource
        fields = ('id', 'url')

    def create(self, validated_data):        
        vid = None
        # try:
        #     vid = Video.objects.create(url=validated_data["url"][1], urlid=validated_data["url"][0])
        #     task_id = async_task('apiv1.task.get_video', vid, sync=False)
        #     print("NEW vid created: " + vid.urlid)
        # except:
        #     vid = Video.objects.get(urlid=validated_data["url"][0])
        #     print("vid exists: " + vid.urlid)
        
        # return vid
        
            # task_id = async_task('apiv1.task.get_video', newvid, sync=False)
            # task = fetch(task_id)

            # # and can be examined
            # if not task.success:
            #     print('An error occurred: {}'.format(task.result))

            # return newvid

    def update(self, instance, validated_data):
        instance.url = validated_data.get('url', instance.url)
        instance.save()
        return instance
    


