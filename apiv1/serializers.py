from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import URLValidator
from .models import MediaResource
from django.db import IntegrityError
import re

from django_q.tasks import async_task, result, fetch

def validate_url(value):
    print("validating")
    regExp = ".*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*"
    x = re.search(regExp, value)
    
    if x == None:
        print("wrong validate")
        raise serializers.ValidationError("Wrong URL")
    
    print(x.group(1) + " test test " + x.group(2))


class MediaResourceSerializer(serializers.Serializer):

    url = serializers.CharField(validators=[validate_url],
                                max_length=None,
                                min_length=None,
                                allow_blank=True,
                                trim_whitespace=True)

    class Meta:
        model = MediaResource
        fields = ('id')

    def create(self, validated_data):
        regExp = ".*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*"
        x = re.search(regExp, validated_data["url"])

        media = MediaResource.objects.create(id=x.group(2))
        media.url = x.group(0)
        media.save()
            # task_id = async_task('apiv1.task.get_video', media, sync=False)
            # print("NEW vid created: " + vid.urlid)
        # except:
            # vid = Video.objects.get(urlid=validated_data["url"][0])
            # print("vid exists: " + vid.urlid)
            # print("error creating model")

        # return vid

        # task_id = async_task('apiv1.task.get_video', newvid, sync=False)
        # task = fetch(task_id)

        # # and can be examined
        # if not task.success:
        #     print('An error occurred: {}'.format(task.result))

        return media

    def update(self, instance, validated_data):
        instance.url = validated_data.get('url', instance.url)
        instance.save()
        return instance
