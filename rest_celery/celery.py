from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_celery.settings')

# Create a Celery instance and configure it using the settings from Django.
app = Celery('rest_celery')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in all installed apps, so you don't have to manually import them.
app.autodiscover_tasks()
