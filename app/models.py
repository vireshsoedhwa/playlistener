from asyncio.log import logger
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.utils.translation import gettext_lazy as _
from django.db.models import Deferrable, UniqueConstraint
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

# from django_q.tasks import async_task, result, fetch

import shutil
import os.path
import logging
logger = logging.getLogger(__name__)


def file_directory_path(instance, filename):
    return ('{0}/{1}').format(instance.id, filename)


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True,
                            blank=False, null=False)

    def __str__(self):
        return str(self.id) + " : " + str(self.name)


class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True,
                            blank=False, null=False)

    def __str__(self):
        return str(self.id) + " : " + str(self.name)


class MediaResource(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    audiofile = models.FileField(upload_to=file_directory_path,
                                 null=True,
                                 blank=True,
                                 max_length=500)
    md5_generated = models.TextField(max_length=32, null=True, blank=True)
    genre = models.TextField(max_length=100, null=True, blank=True)
    artists = models.ManyToManyField(
        Artist, related_name='artists', blank=True)
    tags = models.ManyToManyField(Tag, related_name='artists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " : " + str(os.path.basename(self.audiofile.name)) + " : " + str(self.title)

# signal for deleting
@receiver(post_delete, sender=MediaResource, dispatch_uid="delete_record")
def delete_mediasource_record(sender, instance, **kwargs):
    logger.info(f"Deleting record id#: {instance.id} - {instance.title}")
    try:
        shutil.rmtree(settings.MEDIA_ROOT + str(instance.id))
        logger.info(f"Files deleted id#: {instance.id} - {instance.title}")
    except:
        logger.error("Files could not be deleted")


@receiver(post_save, sender=MediaResource, dispatch_uid="add_record")
def postsave(sender, instance, created, raw, using, update_fields, **kwargs):

    logger.info(f"file saved : {instance.audiofile}")