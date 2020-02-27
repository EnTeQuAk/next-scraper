# -*- coding: utf-8 -*-
from django.contrib.postgres.fields import JSONField
from django.db import models

from werkzeug.http import HTTP_STATUS_CODES

from .utils.html import HTML_VERSION_CHOICES

NEW = 1
RUNNING = 2
ABORTED = 3
COMPLETED = 4


REPORT_STATES = {
    NEW: "New",
    RUNNING: "Running",
    ABORTED: "Aborted",
    COMPLETED: "Completed",
}


class Report(models.Model):
    original_url = models.URLField()
    celery_group_id = models.UUIDField(null=True, default=None)

    state = models.PositiveSmallIntegerField(choices=REPORT_STATES.items(), default=NEW)
    html_version = models.CharField(
        max_length=256, choices=HTML_VERSION_CHOICES.items()
    )
    title = models.CharField(max_length=256)

    # {'h1': 0}
    headings = JSONField(default=dict)

    internal_links = models.PositiveIntegerField(default=0)
    external_links = models.PositiveIntegerField(default=0)

    # We're not breaking this down for simplicity reasons,
    # every error code is "broken" for us as that's mostly what the
    # end-user sees.
    broken_links = models.PositiveIntegerField(default=0)

    contains_login_form = models.BooleanField(default=False)
    status_code = models.PositiveSmallIntegerField(
        null=True, default=None, choices=HTTP_STATUS_CODES.items())
