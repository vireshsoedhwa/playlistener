from django.shortcuts import render
from rest_framework import generics

from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse, FileResponse
from django.core.files import File
from rest_framework.renderers import JSONRenderer

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .serializers import VideoSerializer

import requests
import logging
logger = logging.getLogger(__name__)


# Create your views here.
class submitlink(APIView):
    serializer_class = VideoSerializer
    @extend_schema(
        request=VideoSerializer
    )
    def post(self, request, format=None):
        data = request.data['url']
        # thevid = Video.objects.get(id=38)
        # print(data)
        serializer = VideoSerializer(data={'url': data})
        if serializer.is_valid():
            # serializer.errors
            video = serializer.save()
            print("serializser valid")
            if video.ready:
                file_response = FileResponse(video.audiofile)
                file_response[
                    'Content-Disposition'] = 'attachment; filename="' + video.filename + '"'  
                return file_response
            else:
                return JsonResponse({'id': video.id}, status=201)  


        return JsonResponse(serializer.errors, status=400)
