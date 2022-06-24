from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import URLValidator
from .models import MediaResource
from django.db import IntegrityError
import re

from django_q.tasks import async_task, result, fetch

import logging
logger = logging.getLogger(__name__)

def validate_url(value):
    regExp = ".*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*"
    x = re.search(regExp, value)
    
    if x == None:
        raise serializers.ValidationError("Not a Valid youtube URL: " + value)

class MediaResourceSerializer(serializers.Serializer):

    id = serializers.CharField(validators=[validate_url],
                                max_length=250,
                                min_length=None,
                                allow_blank=True)

    def create(self, validated_data):
        regExp = ".*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*"
        x = re.search(regExp, validated_data["id"])
        video_id = x.group(2)
        # Check if object exists
        num_media = MediaResource.objects.filter(id=video_id).count()
        if num_media != 0:
            return MediaResource.objects.get(id=video_id)
        else:
            media = MediaResource.objects.create(id=video_id)
            media.save()
            return media
        
    def update(self, instance, validated_data):
        instance.url = validated_data.get('url', instance.url)
        instance.save()
        return instance
