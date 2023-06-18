from django.http import HttpResponse, JsonResponse, FileResponse
# from django.core.files import File
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .serializers import MediaResourceSerializer

from .models import MediaResource

from rest_framework.throttling import BaseThrottle, AnonRateThrottle
from django.http import Http404, QueryDict

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from django.conf import settings

import re
import logging

logger = logging.getLogger(__name__)

from .tasks import count_items


decorators = [never_cache, login_required]

@method_decorator(decorators, name='dispatch')
class BaseView(TemplateView):
    # template_name = 'index.html'
    extra_context = {'version': settings.VERSION}

def testfunction(request):

    print("hallo")
    count_items.apply_async()

    return HttpResponse("hello", status=200)


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

    def create(self, request):
        print("Create view")
        # print(request.data)
        # print(request.user)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            result = serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=500)

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
        print("partial update")
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

    @action(detail=True)
    def download(self, request, *args, **kwargs):
        mediaresource = self.get_object()

        if mediaresource.audiofile:
            filename = 'download'
            if mediaresource.title is None:
                filename = mediaresource.audiofile.name
            else:
                filename = mediaresource.title

            file_response = FileResponse(
                mediaresource.audiofile, as_attachment=True, filename=filename
            )

            return file_response

        mediaresource_serializer = self.get_serializer(mediaresource)
        return Response(mediaresource_serializer.data)

    # @action(detail=False, methods=['post'])
    # def multiple_uploads(self, request):
    #     serializer = MediaResourceListSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         # result = serializer.save()
    #         validated = serializer.validated_data.get('valid')
    #         valid_files = []

    #         fileModelObjects = []
    #         for file in validated:
    #             filename = re.sub(r".mp3$", "", file[0].name)
    #             new_file = MediaResource(
    #                 title=filename,
    #                 audiofile=file[0],
    #                 md5_generated=file[1])
    #             fileModelObjects.append(new_file)
    #             valid_files.append(file[0].name)
    #         MediaResource.objects.bulk_create(fileModelObjects)

    #         invalid_files = [
    #             file.name for file in serializer.validated_data.get('invalid')]

    #         already_recorded_files = [
    #             file.name for file in serializer.validated_data.get('already_recorded')]

    #         response = {"valid": valid_files, "invalid": invalid_files,
    #                     "already_recorded": already_recorded_files}

    #         return Response(response, status=200)
    #     return Response(serializer.errors, status=500)
