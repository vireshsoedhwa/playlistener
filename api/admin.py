from django.contrib import admin

# Register your models here.

from .models import MediaResource, DownloadProgress

admin.site.register(MediaResource)
admin.site.register(DownloadProgress)