from django.apps import AppConfig
import os
from django.conf import settings

class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        print("DEBUG: " + str(settings.DEBUG))
        print("PRODUCTION: " + str(settings.PRODUCTION))
        print("GO_PIPELINE_LABEL: " + str(settings.GO_PIPELINE_LABEL))
        print("api has started")

        from django.contrib.auth.models import User

        if not User.objects.filter(username=settings.ADMIN_USERNAME).exists():
            User.objects.create_superuser(
                settings.ADMIN_USERNAME, "admin@example.com", settings.ADMIN_PASSWORD
            )