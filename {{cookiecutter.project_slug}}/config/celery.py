import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.django.local")

app = Celery("config")
app.config_from_object("django.conf:django", namespace="CELERY")
app.autodiscover_tasks()
