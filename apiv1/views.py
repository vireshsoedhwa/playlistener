from django.shortcuts import render
from rest_framework import generics

from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse, FileResponse
from django.core.files import File
from rest_framework.renderers import JSONRenderer

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .serializers import MediaResourceSerializer

from .models import MediaResource
from .youtube import YT

from django_q.tasks import async_task, result, fetch

# import requests
import logging

logger = logging.getLogger(__name__)

# Create your views here.
class submitlink(APIView):
    serializer_class = MediaResourceSerializer

    @extend_schema(request=MediaResourceSerializer,
                   parameters=[
                       OpenApiParameter(name='url',
                                        description='Youtube Url',
                                        required=True,
                                        type=str),
                   ])
    def get(self, request):
        # print(request.GET.get('url', ''))

        serializer = MediaResourceSerializer(
            data={'youtube_id': request.GET.get('url', '')})
        if serializer.is_valid():
            # serializer.errors
            instance = serializer.save()
            print("serializser valid: " + str(instance))

            if instance.download_finished is False:
                # download not finished
                if instance.busy is False:
                    async_task('apiv1.task.get_video', instance, sync=False)
                    return JsonResponse(serializer.data, status=202)
                # download not finished and is in progress
                return JsonResponse(serializer.data, status=201)
            else:
                # download is Finished
                return JsonResponse(serializer.data, status=200)            
        # return HttpResponse("", status=200)
        return JsonResponse(serializer.errors, status=400)

# Create your views here.
class getfile(APIView):
    serializer_class = MediaResource
    @extend_schema(
        request=MediaResource
    )
    def get(self, request, id, format=None):
        try:
            instance = MediaResource.objects.get(id=id)
            
            if instance.audiofile is None:
                return JsonResponse({'id': id}, status=404)
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

class RootPath(APIView):
    # permission_classes = [AllowAny]

    def get(self, request, format=None):

        return JsonResponse({"test":"value"},
                            json_dumps_params={'indent': 2},
                            status=200)

from django.shortcuts import redirect

def view_404(request, exception=None):
    return redirect('/')


def redirect_view(request, namespace, name, slug, actualurl):
    return redirect('/' + actualurl)


def redirect_root(request, namespace, name, slug):
    return redirect('/')
