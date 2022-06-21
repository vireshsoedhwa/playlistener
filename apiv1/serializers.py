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
        raise serializers.ValidationError("Not a Valid URL: " + value)

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

        try:
            media = MediaResource.objects.create(id=x.group(2))
            media.url = x.group(0)
            media.save()
            return media
        except (IntegrityError) as e:
            raise serializers.ValidationError("URL Exists: " + validated_data["url"])
        except AttributeError as e:
            raise serializers.ValidationError("Not a Valid URL: " + validated_data["url"])
        
    def update(self, instance, validated_data):
        instance.url = validated_data.get('url', instance.url)
        instance.save()
        return instance
