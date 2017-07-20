from __future__ import absolute_import
import os
from celery import Celery

from django.conf import settings
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IrisOnline.settings')

app = Celery('IrisOnline', broker='redis://localhost:6379/0',include=[
    "IrisOnline.tasks",
    "order_management.tasks"
])

app.conf.update(
        CELERY_TIMEZONE = 'Asia/Manila'
)

app.conf.update(
    broker_url = 'redis://localhost:6379',
    result_backend = 'redis://localhost:6379',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Manila',

)
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'IrisOnline.tasks.printthis',
        'schedule':(crontab(hour=13,minute=33)),
    },
}
# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


