# Create your tasks here

from .models import MediaResource
import os
from celery import shared_task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

@shared_task
def count_items():

    # for file in os.listdir("/mydir"):
    logger.info("IT RRAN THE TASk Rannnn has started")
    print("why no logs ")
    return MediaResource.objects.count()


