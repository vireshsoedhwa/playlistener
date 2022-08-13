from asyncio.log import logger
from pickle import FALSE
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.utils.translation import gettext_lazy as _
from django.db.models import Deferrable, UniqueConstraint
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

import os

from django_q.tasks import async_task, result, fetch
import shutil
import logging
logger = logging.getLogger(__name__)



def file_directory_path(instance, filename):
    return ('{0}/{1}').format(instance.id, filename)


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, blank=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, blank=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class MediaResource(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    audiofile = models.FileField(upload_to=file_directory_path,
                                 null=True,
                                 blank=True,
                                 max_length=500)
    original_duration = models.DurationField(null=True, blank=True)
    audiofile_432 = models.FileField(upload_to=file_directory_path,
                                     null=True,
                                     blank=True,
                                     max_length=500)
    converted_432_duration = models.DurationField(null=True, blank=True)
    md5_generated = models.TextField(max_length=32, null=True, blank=True)
    genre = models.TextField(max_length=100, null=True, blank=True)
    artists = models.ManyToManyField(Artist, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " : " + str(self.title) + " - " + str(os.path.basename(self.audiofile.name))  


class YoutubeMediaResource(models.Model):
    class Status(models.TextChoices):
        NEW = 'NEW', _('New')
        BUSY = 'BUSY', _('Busy')
        FAILED = 'FAILED', _('Failed')
        DONE = 'DONE', _('Done')

    youtube_id = models.TextField(primary_key=True, max_length=200)
    mediaresource = models.OneToOneField(
        MediaResource,
        related_name='youtubedata',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    error = models.TextField(max_length=500, null=True,
                             blank=True,)
    status = models.CharField(
        max_length=7, choices=Status.choices, default=Status.NEW)
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
        if instance.status == "NEW":
            instance.status = "BUSY"
            instance.save()
            async_task('api.task.get_video', mediaresource, sync=False)
    else:
        pass
        # TODO retry download here on user request

# signal for deleting
@receiver(post_delete, sender=MediaResource, dispatch_uid="delete_yt_archive_record")
def delete_mediasource_record(sender, instance, **kwargs):
    logger.info(f"Deleting record id#:{instance.id}")
    try:
        shutil.rmtree(settings.MEDIA_ROOT + str(instance.id))
    except:
        logger.error("Files could not be deleted")