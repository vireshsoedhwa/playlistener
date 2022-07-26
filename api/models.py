from django.db import models
from django.core.files.storage import FileSystemStorage
from django.db.models import Deferrable, UniqueConstraint
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from django_q.tasks import async_task, result, fetch

import re


def file_directory_path(instance, filename):

    return ('{0}/{1}').format(instance.id, filename)


class MediaResource(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    audiofile = models.FileField(upload_to=file_directory_path,
                                 null=True,
                                 blank=True,
                                 max_length=500)
    audiofile_432 = models.FileField(upload_to=file_directory_path,
                                 null=True,
                                 blank=True,
                                 max_length=500)
    genre = models.TextField(max_length=100, null=True, blank=True)
    artist = models.TextField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " : " + str(self.title)

# signal for updating

# # signal for deleting
@receiver(post_delete, sender=MediaResource, dispatch_uid="delete_yt_archive_record")
def delete_record(sender, instance, **kwargs):

    print(f"Deleted ID:{instance.id}")

class YoutubeMediaResource(models.Model):
    youtube_id = models.TextField(primary_key=True, max_length=200)
    mediaresource = models.OneToOneField(
        MediaResource,
        related_name='youtube_data',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    download_finished = models.BooleanField(null=True,
                                            blank=True,
                                            default=False)
    busy = models.BooleanField(null=True, blank=True, default=False)
    downloadprogress = models.DecimalField(max_digits=3, decimal_places=0, blank=True,
                                   default=0)
    eta = models.DecimalField(max_digits=5, decimal_places=0, blank=True,
                              default=0)
    elapsed = models.DecimalField(max_digits=5, decimal_places=0, blank=True,
                                  default=0)
    speed = models.DecimalField(max_digits=10, decimal_places=0, blank=True,
                                default=0)

@receiver(post_save, sender=YoutubeMediaResource, dispatch_uid="create_mediaresource")
def checkdownload(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        mediaresource = MediaResource.objects.create()
        mediaresource.save()
        instance.mediaresource = mediaresource
        instance.save()
        if instance.download_finished is False:
            if instance.busy is False:
                async_task('api.task.get_video', mediaresource, sync=False)
    else:
        pass