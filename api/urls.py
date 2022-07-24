from django.urls import path
from django.conf import settings
from . import views

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('submitlink', views.submitlink.as_view()),
    path('getfile/<id>', views.getfile.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
        path('', SpectacularSwaggerView.as_view(url_name='schema'),
             name='swagger-ui'),
        path('schema', SpectacularAPIView.as_view(), name='schema'),
    ]
