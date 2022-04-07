from django.db import models
from django.core.files.storage import FileSystemStorage
from django.db.models import Deferrable, UniqueConstraint
from django.db.models.signals import post_save
from django.dispatch import receiver

import re

# Create your models here.

# def validate_url(url):
#     try:
#         URLValidator(url)
#     except ValidationError:
#         return False
#     return True

def file_directory_path(instance, filename):
    return '/code/dl/{0}/{1}'.format(instance.urlid, instance.filename)


def my_callback(sender, **kwargs):
    print("Request finished!dsaffffffff")

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    urlid = models.TextField(max_length=200, null=True, blank=True)
    filename = models.TextField(max_length=200, null=True, blank=True)
    ready = models.BooleanField(null=True, blank=True, default=False)
    downloaded_bytes = models.TextField(max_length=200,null=True,blank=True)
    total_bytes = models.TextField(max_length=200,null=True,blank=True)
    status = models.TextField(max_length=200, null=True,blank=True)
    audiofile = models.FileField(upload_to=file_directory_path, null=True, blank=True)
    # videofile = models.FileField(upload_to=file_directory_path, null=True, blank=True)
    # state = models.DecimalField(decimal_places=0, max_digits=2, null=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
        UniqueConstraint(fields=['urlid'], name="vid-id")
        ]

    def create_urlid(self, **kwargs):
        # instance
        x = re.search("(https?://)?(www\.)?youtube\.(com|ca)/watch\?v=([-\w]+)", self.url)
        # print(x.group(4))
        self.urlid = x.group(4)
        self.save()
        # self.urlid = x
        

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