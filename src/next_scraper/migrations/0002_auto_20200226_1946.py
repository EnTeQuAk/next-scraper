# Generated by Django 3.0.3 on 2020-02-26 19:46

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("next_scraper", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="report",
            name="headings",
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]