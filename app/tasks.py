# Create your tasks here

from .models import MediaResource
import os
import glob
from celery import shared_task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from .serializers import MediaResourceSerializer

@shared_task
def count_items():

    root_dir = "/code/data/"
    for filename in glob.iglob(root_dir + '**/*.mp3', recursive=True):
        logger.info(filename)

    # logger.info("IT RRAN THE TASk Rannnn has started")

    return MediaResource.objects.count()


