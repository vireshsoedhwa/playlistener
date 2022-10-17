from django.contrib import admin

# Register your models here.

from .models import MediaResource, Artist, Tag
admin.site.site_header = "PLAPI Admin"
admin.site.site_title = "PLAPI site admin"
admin.site.register(MediaResource)
admin.site.register(Artist)
admin.site.register(Tag)