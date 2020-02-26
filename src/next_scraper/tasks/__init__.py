import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "next_scraper.conf.development")

from django.conf import settings

from celery import Celery

celery = Celery("next_scraper")

celery.config_from_object("django.conf:settings", namespace="CELERY")
celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
task = celery.task
