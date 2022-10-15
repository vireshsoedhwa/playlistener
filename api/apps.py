from django.apps import AppConfig
import os
from django.conf import settings
import sys
import logging
logger = logging.getLogger(__name__)

class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):

        if 'runserver' in sys.argv or 'playlistenerapi.asgi:application' in sys.argv:
            print("DEBUG: " + str(settings.DEBUG))
            print("api has started")

            
            from django.contrib.auth.models import User

            if not User.objects.filter(username=settings.ADMIN_USERNAME).exists():
                User.objects.create_superuser(
                    settings.ADMIN_USERNAME, "admin@example.com", settings.ADMIN_PASSWORD
                )