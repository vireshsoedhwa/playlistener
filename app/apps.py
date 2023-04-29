from django.apps import AppConfig
import os
from django.conf import settings
import sys
import logging
logger = logging.getLogger(__name__)

class ApiConfig(AppConfig):
    name = 'app'
    def ready(self):

        if 'runserver' in sys.argv or 'playlistenerapi.wsgi' in sys.argv:
            logger.info("DEBUG: " + str(settings.DEBUG))
            logger.info("plapi has started")

            if 'runserver' in sys.argv:
                logger.warn("running in DEV mode")
            
            from django.contrib.auth.models import User

            if not User.objects.filter(username=settings.ADMIN_USERNAME).exists():
                User.objects.create_superuser(
                    settings.ADMIN_USERNAME, "admin@example.com", settings.ADMIN_PASSWORD
                )