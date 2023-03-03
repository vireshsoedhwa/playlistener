from django.urls import path, include
from django.conf import settings
from . import views
from .views import MediaResourceViewSet
from rest_framework.routers import DefaultRouter
from .views import BaseView
from django.contrib.auth import views as auth_views

router = DefaultRouter()

router.register(r'mediaresources', MediaResourceViewSet,
                basename="mediaresources")

urlpatterns = [
    path('', BaseView.as_view(template_name='index.html'), name='index'),
    path('home', BaseView.as_view(template_name='index.html'), name='index'),
    path('create', BaseView.as_view(template_name='index.html'), name='index'),
    path('', include(router.urls)),
    # path("accounts/", include("django.contrib.auth.urls")),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(), name='logout'),
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='index.html'),
    ),
]
