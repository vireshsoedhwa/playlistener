from django.contrib import admin

# Register your models here.

from .models import MediaResource, YoutubeMediaResource

admin.site.register(MediaResource)
admin.site.register(YoutubeMediaResource)