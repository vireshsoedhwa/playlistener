import re
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework import generics

from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse, FileResponse
# from django.core.files import File
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
# from drf_spectacular.types import OpenApiTypes
from .serializers import SubmitLinkSerializer, GetfileSerializer, ListSerializer, ListRequestSerializer

from .models import MediaResource
from .youtube import YT

from django_q.tasks import async_task, result, fetch

from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle
from django.http import Http404, QueryDict

# import requests
import logging

from api import serializers
logger = logging.getLogger(__name__)


class OncePerDayUserThrottle(UserRateThrottle):
    rate = '5/day'


@api_view(['GET'])
@throttle_classes([OncePerDayUserThrottle])
def view(request):
    return Response({"message": "Hello for today! See you tomorrow!"})


class Submitlink(APIView):
    # serializer_class = SubmitLinkSerializer

    # @extend_schema(request=SubmitLinkSerializer,
    #                parameters=[
    #                    OpenApiParameter(name='url',
    #                                     description='Youtube Url',
    #                                     required=True,
    #                                     type=str),
    #                ])
    def sanitize_url(self, url):
        # return Response("get")
        try:
            regExp = ".*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*"
            x = re.search(regExp, url)
            video_id = x.group(2)
            return video_id
        except:
            raise Http404

    def get_object(self, youtube_id):
        try:
            print("existing one")
            return MediaResource.objects.get(youtube_id=youtube_id)
        except MediaResource.DoesNotExist:
            print("new one")
            return None

    def put(self, request):
        url = request.query_params.get("youtube_id", None)
        if url:
            youtube_id = self.sanitize_url(url)
            print(youtube_id)
            existing_object = self.get_object(youtube_id)
            print(existing_object)
            print(request.query_params)

            query_dict = request.query_params.copy()
            query_dict['youtube_id'] = youtube_id

            print(query_dict)
            serializer = SubmitLinkSerializer(
                existing_object, data=query_dict, partial=True)

            # print("yeah")
            if serializer.is_valid():
                instance = serializer.save()
                # return Response("BLABLA")

                return Response(serializer.data)
            return Response(serializer.errors, status=400)

        return Response("no url provided", status=400)

class Getfile(APIView):
    serializer_class = GetfileSerializer

    @extend_schema(
        request=MediaResource
    )
    def get(self, request, id, format=None):
        try:
            instance = MediaResource.objects.get(id=id)

            if instance.audiofile is None:
                return JsonResponse({'id': id, 'download_finished': instance.download_finished, 'busy': instance.busy}, status=404)

            filename = 'download'
            if instance.title is None:
                filename = instance.audiofile.name
            else:
                filename = instance.title

            file_response = FileResponse(instance.audiofile)
            file_response[
                'Content-Disposition'] = 'attachment; filename="' + filename
            return file_response
        except:
            return JsonResponse({'id': id}, status=404)


class List(APIView):
    def get(self, request, format=None):
        if "count" in request.query_params:
            serializer = ListRequestSerializer(
                data={'count': request.query_params['count']})
            if serializer.is_valid():
                return querysetresponse(serializer.validated_data['count'])
        return querysetresponse(0)


def querysetresponse(count):
    if count == 0:
        count = None
    queryset = MediaResource.objects.all()[:count]
    listserializer = ListSerializer(queryset, many=True)
    return Response(listserializer.data)


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
