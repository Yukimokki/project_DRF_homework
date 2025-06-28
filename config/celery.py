from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Setting env variable for the project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Celery object creation
app = Celery('config')

# Settings loading from Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatic search and task registration from files tasks.py in Django app
app.autodiscover_tasks()

# Setting for pool in Windows
app.conf.worker_pool = 'solo'
