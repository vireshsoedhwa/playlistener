from django.urls import path, include
from django.conf import settings
from . import views
from .views import MediaResourceViewSet
from rest_framework.routers import DefaultRouter

# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('submitlink', views.Submitlink.as_view()),
    path('getfile/<int:id>', views.Getfile.as_view()),
    # path('list', views.List.as_view()),
]

# if settings.DEBUG:
#     urlpatterns += [
#         path('', SpectacularSwaggerView.as_view(url_name='schema'),
#              name='swagger-ui'),
#         path('schema', SpectacularAPIView.as_view(), name='schema'),
#     ]

router = DefaultRouter()

router.register(r'mediaresources', MediaResourceViewSet,
                basename="mediaresources")

urlpatterns += [
    path('', include(router.urls)),
]

# mediaresource_list = MediaResourceViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# mediaresource_detail = MediaResourceViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
# mediaresource_highlight = MediaResourceViewSet.as_view({
#     'get': 'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])

# urlpatterns += format_suffix_patterns([
#     path('', RootPath),
#     path('mediaresource/', mediaresource_list, name='mediaresource-list'),
#     path('mediaresource/<int:pk>/', mediaresource_detail, name='mediaresource-detail'),
#     path('mediaresource/<int:pk>/highlight/', mediaresource_highlight, name='mediaresource-highlight'),
# ])
