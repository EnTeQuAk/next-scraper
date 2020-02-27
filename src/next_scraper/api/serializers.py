from rest_framework import serializers

from next_scraper.models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        exclude = ('celery_group_id',)
