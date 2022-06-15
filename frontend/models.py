from django.db import models
from django.core.files.storage import FileSystemStorage
from django.db.models import Deferrable, UniqueConstraint
from django.db.models.signals import post_save
from django.dispatch import receiver

import re


def file_directory_path(instance, filename):
    return '/code/dl/{0}/{1}'.format(instance.id, instance.filename)


def my_callback(sender, **kwargs):
    print("")


class Resource(models.Model):
    id = models.TextField(primary_key=True, max_length=200, blank=True)
    title = models.TextField(max_length=200, null=True, blank=True)
    download_finished = models.BooleanField(null=True,
                                            blank=True,
                                            default=False)
    audiofile_converted = models.BooleanField(null=True,
                                              blank=True,
                                              default=False)
    status = models.TextField(max_length=200, null=True, blank=True)
    original_videofile = models.FileField(upload_to=file_directory_path,
                                          null=True,
                                          blank=True)
    original_audiofile = models.FileField(upload_to=file_directory_path,
                                          null=True,
                                          blank=True)
    converted_audiofile = models.FileField(upload_to=file_directory_path,
                                           null=True,
                                           blank=True)

    # videofile = models.FileField(upload_to=file_directory_path, null=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [UniqueConstraint(fields=['id'], name="vid-id")]

    def __str__(self):
        return str(self.id)


# class TransactionDetail(models.Model):
#     product = models.ForeignKey(Product)

# # method for updating
# @receiver(post_save, sender=Video, dispatch_uid="update_urlslug")
# def update_urlid(sender, instance, **kwargs):
#     # instance.product.stock -= instance.amount
#     print("TEEEEEEEST")
#     post_save.disconnect(update_urlid, sender=Video)
#     instance.save()
#     post_save.connect(update_urlid, sender=Video)