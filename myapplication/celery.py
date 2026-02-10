import os
from celery import Celery

# Defines to use django settings module for celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapplication.settings")
app = Celery("celery_application")
app.config_from_object("django.conf:settings", namespace="CELERY")  

#Look inside every app listed in INSTALLED_APPS
#and automatically import any tasks.py file found
app.autodiscover_tasks()

