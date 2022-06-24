from django.apps import AppConfig
import os
from django.conf import settings

class Apiv1Config(AppConfig):
    name = 'apiv1'

    def ready(self):
        print("DEBUG: " + str(settings.DEBUG))
        print("apiv1 has started")
