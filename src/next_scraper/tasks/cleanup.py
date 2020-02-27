from datetime import timedelta

from django.utils import timezone

from ..models import Report
from . import task


@task
def cleanup_reports():
    """Cleanup reports that are older than 24 hours."""
    Report.objects.filter(
        created__gt=timezone.now() - timedelta(days=1)).delete()
