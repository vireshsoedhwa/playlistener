from django.shortcuts import render
from rest_framework import generics

from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse, FileResponse
from django.core.files import File
from rest_framework.renderers import JSONRenderer

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
# from .serializers import ResourceSerializer

# from .models import Resource

import requests
import logging

logger = logging.getLogger(__name__)


# Create your views here.
class submitlink(APIView):
    # serializer_class = ResourceSerializer

    # @extend_schema(request=ResourceSerializer)
    def post(self, request, format=None):
        data = request.data['url']
        # thevid = Video.objects.get(id=38)
        print(data)
        # serializer = ResourceSerializer(data={'url': data})
        # if serializer.is_valid():
        #     # serializer.errors
        #     video = serializer.save()
        #     print("serializser valid")
        #     if video.ready:
        #         file_response = FileResponse(video.audiofile)
        #         file_response[
        #             'Content-Disposition'] = 'attachment; filename="' + video.filename + '"'
        #         return file_response
        #     else:
        #         return JsonResponse({'id': video.id}, status=201)

        # return JsonResponse(serializer.errors, status=400)


# Create your views here.
class getfile(APIView):
    # serializer_class = VideoSerializer
    # @extend_schema(
    #     request=VideoSerializer
    # )
    def get(self, request, id, format=None):
        # data = request.data['url']
        # # thevid = Video.objects.get(id=38)
        # # print(data)
        # serializer = VideoSerializer(data={'url': data})
        # if serializer.is_valid():
        #     # serializer.errors
        #     video = serializer.save()
        #     print("serializser valid")
        #     if video.ready:
        #         file_response = FileResponse(video.audiofile)
        #         file_response[
        #             'Content-Disposition'] = 'attachment; filename="' + video.filename + '"'
        #         return file_response
        #     else:
        #         return JsonResponse({'id': video.id}, status=201)

        # vid = Video.objects.create(id=self.Newdownloadprocess.url)
        try:
            vid = Resource.objects.get(id=id)
        
            print("ayooo")
            print(vid)
            print(vid.original_audiofile.path)

            file_response = FileResponse(vid.original_audiofile)
            file_response[
                'Content-Disposition'] = 'attachment; filename="' + vid.title + 'mp3"'
            return file_response
        except:
            return JsonResponse({'foo': 'bar'}, status=404)

# class getvideo(APIView):
#     def get(self, request, id, format=None):
#         try:
#             vid = Video.objects.get(id=id)
        
#             print("ayooo")
#             print(vid)
#             print(vid.original_videofile.path)

#             file_response = FileResponse(vid.original_videofile)
#             file_response[
#                 'Content-Disposition'] = 'attachment; filename="' + vid.title + 'mp3"'
#             return file_response
#         except:
#             return JsonResponse({'foo': 'bar'}, status=404)