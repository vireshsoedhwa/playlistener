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

from .serializers import MediaResourceSerializer

from .models import MediaResource
# from .youtube import YT

# from django_q.tasks import async_task, result, fetch
# from django.core.exceptions import ObjectDoesNotExist

from rest_framework.throttling import BaseThrottle, AnonRateThrottle
from django.http import Http404, QueryDict


from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import renderers

import logging
import random

logger = logging.getLogger(__name__)


class PostAnonRateThrottle(AnonRateThrottle):
    scope = 'post_anon'

    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        return super().allow_request(request, view)


class MediaResourceViewSet(viewsets.ModelViewSet):
    queryset = MediaResource.objects.all()
    serializer_class = MediaResourceSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    throttle_classes = [PostAnonRateThrottle]

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

    def partial_update(self, request, pk=None):

        try:
            record_to_update = MediaResource.objects.get(pk=pk)
        except MediaResource.DoesNotExist:
            return Response("record not found", status=400)
        mediaresource_serializer = self.get_serializer(
            record_to_update, request.data, partial=True)

        if mediaresource_serializer.is_valid(raise_exception=True):
            result = mediaresource_serializer.save()
            result.save()
            return Response(mediaresource_serializer.data, status=200)
        return Response(mediaresource_serializer.errors, status=500)
    # def create(self, request):
    #     validlist = []
    #     for audiofile in request.data.getlist('audiofile'):
    #         mediaresource_serializer = self.get_serializer(
    #             data={'audiofile': audiofile})
    #         if mediaresource_serializer.is_valid():
    #             mediaresource_serializer.save()
    #             validlist.append(str(audiofile))
    #         else:
    #             validlist.append(mediaresource_serializer.errors)
    #     return Response(validlist)

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
