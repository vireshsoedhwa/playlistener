from django.apps import AppConfig
import os
from django.conf import settings

class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        print("DEBUG: " + str(settings.DEBUG))
        print("PRODUCTION: " + str(settings.PRODUCTION))
        print("api has started")
