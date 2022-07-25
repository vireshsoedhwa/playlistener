from django.db import models
from django.core.files.storage import FileSystemStorage
from django.db.models import Deferrable, UniqueConstraint
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from django_q.tasks import async_task, result, fetch

import re


def file_directory_path(instance, filename):
    return ('{0}{1}/{2}').format(settings.MEDIA_ROOT, instance.id, instance.filename)


class MediaResource(models.Model):
    id = models.AutoField(primary_key=True)
    youtube_id = models.TextField(unique=True, max_length=200, blank=True)
    title = models.TextField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    download_finished = models.BooleanField(null=True,
                                            blank=True,
                                            default=False)
    busy = models.BooleanField(null=True, blank=True, default=False)
    audiofile = models.FileField(upload_to=file_directory_path,
                                 null=True,
                                 blank=True,
                                 max_length=500)
    genre = models.TextField(max_length=100, null=True, blank=True)
    artist = models.TextField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     constraints = [UniqueConstraint(fields=['id'], name="vid-id")]

    def __str__(self):
        return str(self.id)

# signal for updating


@receiver(post_save, sender=MediaResource, dispatch_uid="update_urlslug")
def checkdownload(sender, instance, created, raw, using, update_fields, **kwargs):
    # print("TEEEEEEEST")
    # print("sender " + str(sender))
    # print("instance " + str(instance))
    # print("created  " + str(created))
    # print("raw " + str(raw))
    # print("using " + str(using))
    # print("update fields " + str(update_fields))

    if created:
        if instance.download_finished is False:
            if instance.busy is False:
                async_task('api.task.get_video', instance, sync=False)
    else:
        pass


# # signal for deleting
@receiver(post_delete, sender=MediaResource, dispatch_uid="delete_yt_archive_record")
def delete_record(sender, instance, **kwargs):

    print(f"Deleted ID:{instance.id} with youtube id {instance.youtube_id}")


class DownloadProgress(models.Model):
    object = models.OneToOneField(
        MediaResource,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    progress = models.DecimalField(max_digits=3, decimal_places=0, blank=True,
                                   default=False)
    eta = models.DecimalField(max_digits=5, decimal_places=0, blank=True,
                              default=False)
    elapsed = models.DecimalField(max_digits=5, decimal_places=0, blank=True,
                                  default=False)
    speed = models.DecimalField(max_digits=10, decimal_places=0, blank=True,
                                default=False)

    # def __str__(self):
    #     return str(object.id) + " : " + str(self.progress)
