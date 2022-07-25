from django.urls import path
from django.conf import settings
from . import views

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('submitlink', views.Submitlink.as_view()),
    path('getfile/<int:id>', views.Getfile.as_view()),
    path('list', views.List.as_view()),
    path('test', views.view)
]

if settings.DEBUG:
    urlpatterns += [
        path('', SpectacularSwaggerView.as_view(url_name='schema'),
             name='swagger-ui'),
        path('schema', SpectacularAPIView.as_view(), name='schema'),
    ]
