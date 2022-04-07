from django.urls import path
# from django.conf.urls import url
from . import views

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # path('', views.ImageItemListCreate.as_view() ),
    # path('', views.ListAllBThreads.as_view() ),
    path('submitlink', views.submitlink.as_view()),
    # path('getfile', views.getfile.as_view()),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]
