# Create your tasks here

from .models import MediaResource

from celery import shared_task

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def count_items():

    logger.info("IT RRAN THE TASk Rannnn has started")

    return MediaResource.objects.count()


