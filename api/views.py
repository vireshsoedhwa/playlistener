from email.mime import audio
import re
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework import generics

from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse, FileResponse
# from django.core.files import File
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .serializers import SubmitLinkSerializer, GetfileSerializer, MediaResourceSerializer, YoutubeMediaResourceSerializer

from .models import MediaResource, YoutubeMediaResource
from .youtube import YT

from django_q.tasks import async_task, result, fetch
# from django.core.exceptions import ObjectDoesNotExist

# from rest_framework.decorators import api_view, throttle_classes
# from rest_framework.throttling import UserRateThrottle
from django.http import Http404, QueryDict


from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import renderers

import logging

from api import serializers
logger = logging.getLogger(__name__)


class MediaResourceViewSet(viewsets.ModelViewSet):
    queryset = MediaResource.objects.all()
    serializer_class = MediaResourceSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def list(self, request):
        show = None
        if "show" in request.query_params:
            try:
                if int(request.query_params['show']) == 0:
                    show = None
                else:
                    show = int(request.query_params['show'])
            except:
                show = None
        recent = MediaResource.objects.all().order_by('-created_at')[:show]
        serializer = self.get_serializer(recent, many=True)
        return Response(serializer.data)

    def create(self, request):
        validlist = []
        for audiofile in request.data.getlist('audiofile'):
            mediaresource_serializer = self.get_serializer(
                data={'audiofile': audiofile})
            if mediaresource_serializer.is_valid():
                mediaresource_serializer.save()
                validlist.append(str(audiofile))
            else:
                validlist.append(mediaresource_serializer.errors)
        return Response(validlist)

    @action(detail=True)
    def download(self, request, *args, **kwargs):
        mediaresource = self.get_object()

        if mediaresource.audiofile:
            filename = 'download'
            if mediaresource.title is None:
                filename = mediaresource.audiofile.name
            else:
                filename = mediaresource.title

            file_response = FileResponse(mediaresource.audiofile)
            file_response[
                'Content-Disposition'] = 'attachment; filename="' + filename + '.mp3"'
            return file_response

        mediaresource_serializer = self.get_serializer(mediaresource)
        return Response(mediaresource_serializer.data)


class YoutubeMediaResourceViewSet(viewsets.ModelViewSet):
    queryset = YoutubeMediaResource.objects.all()
    serializer_class = YoutubeMediaResourceSerializer

    def create(self, request):

        youtube_media_resource_serializer = self.get_serializer(
            data=request.data)

        if youtube_media_resource_serializer.is_valid(raise_exception=True):
            new_id = youtube_media_resource_serializer.save()
            return Response(youtube_media_resource_serializer.data)
        return Response(youtube_media_resource_serializer.errors)


# class Submitlink(APIView):
#     def sanitize_url(self, url):
#         try:
#             regExp = ".*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*"
#             x = re.search(regExp, url)
#             video_id = x.group(2)
#             return video_id
#         except:
#             raise Http404

#     def get_object(self, youtube_id):
#         try:
#             youtube_media_resource = YoutubeMediaResource.objects.get(
#                 youtube_id=youtube_id)
#             return youtube_media_resource
#         except YoutubeMediaResource.DoesNotExist:
#             return None

#     def put(self, request):
#         url = request.query_params.get("youtube_id", None)
#         if url:
#             youtube_id = self.sanitize_url(url)
#             existing_object = self.get_object(youtube_id)
#             query_dict = request.query_params.copy()
#             query_dict['youtube_id'] = youtube_id
#             serializer = SubmitLinkSerializer(
#                 existing_object, data=query_dict, partial=True)

#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=400)
#         return Response("no url provided", status=400)


# class Getfile(APIView):
#     serializer_class = GetfileSerializer

#     @extend_schema(
#         request=MediaResource
#     )
#     def get(self, request, id, format=None):

#         serializer = GetfileSerializer(data={'id': id})

#         if serializer.is_valid():
#             try:
#                 instance = MediaResource.objects.get(pk=id)
#                 if instance.audiofile:
#                     filename = 'download'
#                     if instance.title is None:
#                         filename = instance.audiofile.name
#                     else:
#                         filename = instance.title
#                     file_response = FileResponse(instance.audiofile)
#                     file_response[
#                         'Content-Disposition'] = 'attachment; filename="' + filename
#                     return file_response
#                 else:
#                     return JsonResponse({'id': id, 'download_finished': instance.youtube_data.download_finished, 'busy': instance.youtube_data.busy}, status=404)
#             except MediaResource.DoesNotExist:
#                 return Response(str(id)+' does not exist', status=404)
#         return JsonResponse(serializer.errors, status=400)

# # views.py
# class FileUploadView(APIView):
#     parser_classes = [MultiPartParser]

#     def put(self, request, filename, format=None):
#         file_obj = request.data['file']
#         # ...
#         # do some stuff with uploaded file
#         # ...
#         return Response(status=204)


class RootPath(APIView):
    # permission_classes = [AllowAny]
    def get(self, request, format=None):
        return JsonResponse({"test": "value"},
                            json_dumps_params={'indent': 2},
                            status=200)


def view_404(request, exception=None):
    return redirect('/')


def redirect_view(request, namespace, name, slug, actualurl):
    return redirect('/' + actualurl)


def redirect_root(request, namespace, name, slug):
    return redirect('/')
