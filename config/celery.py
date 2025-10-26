import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from celery import Celery
from django.conf import settings

app = Celery('config')

app.config_from_object(settings.CELERY)

app.autodiscover_tasks()
