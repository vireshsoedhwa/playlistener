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
        print(request.GET.get('url', ''))

        serializer = MediaResourceSerializer(
            data={'url': request.GET.get('url', '')})
        if serializer.is_valid():
            # serializer.errors
            media = serializer.save()
            print("serializser valid: " + str(media))
            # if video.ready:
            #     file_response = FileResponse(video.audiofile)
            #     file_response[
            #         'Content-Disposition'] = 'attachment; filename="' + video.filename + '"'
            #     return file_response
            # else:
            #     return JsonResponse({'id': video.id}, status=201)

            async_task('apiv1.task.get_video', media, sync=False)
            #         # task = fetch(task_id)
            #         # # and can be examined
            #         # if not task.success:
            #         #     print('An error occurred: {}'.format(task.result))
            #         #     return False
            #         print("NEW vid created: " + vid.urlid)

            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


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


class RootPath(APIView):
    # permission_classes = [AllowAny]

    def get(self, request, format=None):
        # from .models import StatusResponse
        # from .serializers import StatusResponseSerializer

        # status = StatusResponse(version_number=settings.GIT_TAG)
        # serializer = StatusResponseSerializer(status)

        # return JsonResponse(serializer.data,
        #                     json_dumps_params={'indent': 2},
        #                     status=200)

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
