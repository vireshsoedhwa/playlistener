import os

from celery.utils.log import get_task_logger
tasklogger = get_task_logger(__name__)

import logging
orglogger = logging.getLogger(__name__)

from celery import Celery
# from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'playlistenerapi.settings')
app = Celery('playlistenerapi')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')

# app.conf.beat_schedule = {
#     'add-every-10-seconds': {
#         'task': 'test',
#         'schedule': 10.0
#     },
# }

app.conf.timezone = 'America/Vancouver'


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')


@app.task
def test(arg):

    orglogger.debug("PLEASEEEJJEJEJE")
    tasklogger.debug("whahhdhahd")
    
    print(arg)
    print("dfashfasd")