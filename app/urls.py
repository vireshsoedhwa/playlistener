from django.urls import path, include
from django.conf import settings
from . import views
from .views import MediaResourceViewSet
from rest_framework.routers import DefaultRouter
from .views import BaseView

router = DefaultRouter()

router.register(r'mediaresources', MediaResourceViewSet,
                basename="mediaresources")

urlpatterns = [
    path('', BaseView.as_view(template_name='index.html'), name='home'),
    # path('', include(router.urls)),
]

