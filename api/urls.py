from django.urls import path, include
from django.conf import settings
from . import views
from .views import MediaResourceViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'mediaresources', MediaResourceViewSet,
                basename="mediaresources")

urlpatterns = [
    path('', include(router.urls)),
]

