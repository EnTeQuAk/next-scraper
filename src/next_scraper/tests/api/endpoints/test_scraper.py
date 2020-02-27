from unittest import mock

from django.urls import reverse
from rest_framework.test import APIClient

import pytest
import responses
from next_scraper.models import COMPLETED, Report


@pytest.fixture(autouse=True)
def example_page_structure():
    responses.add(
        responses.GET,
        'https://example.com',
        content_type='text/html',
        body='<!doctype html><html><a href="/broken">foo</a><a href="/success"></a>'
    )
    responses.add(
        responses.GET,
        'https://example.com/broken',
        content_type='text/html',
        status=404,
        body='Not Found'
    )
    responses.add(
        responses.GET,
        'https://example.com/success',
        content_type='text/html',
        body=''
    )


@pytest.mark.django_db
def test_start_simple():
    url = reverse("api:start-scraper")

    assert Report.objects.count() == 0

    response = APIClient().post(url, data={'url': 'https://example.com'})

    assert response.status_code == 201

    # There's only one report so we can rely on .get() which will then fail
    # in case that assumption is wrong.
    report = Report.objects.get()
    assert report.state == COMPLETED
    assert report.status_code == 200
    assert report.broken_links == 1
    assert report.internal_links == 2
    assert report.external_links == 0
    assert report.celery_group_id is not None
    assert not report.may_contain_login_form
    assert report.html_version == 'html5'
    assert report.title == ''
    assert report.headings == {
        "h1": 0,
        "h2": 0,
        "h3": 0,
        "h4": 0,
        "h5": 0,
        "h6": 0
    }


@pytest.mark.django_db
def test_start_no_url():
    url = reverse("api:start-scraper")

    assert Report.objects.count() == 0

    response = APIClient().post(url, data={})

    assert response.status_code == 400
    assert response.json() == {
        "error": "URL is required"
    }


@pytest.mark.django_db
def test_start_duplicate_report():
    url = reverse("api:start-scraper")

    Report.objects.create(original_url="https://example.com")

    response = APIClient().post(url, data={"url": "https://example.com"})

    assert response.status_code == 409


@pytest.mark.django_db
def test_report_simple():
    response = APIClient().post(
        reverse("api:start-scraper"),
        data={"url": "https://example.com"})
    assert response.status_code == 201

    url = reverse("api:report-detail", kwargs={'url': "https://example.com"})

    response = APIClient().get(url)
    assert response.status_code == 200

    assert response.json() == {
        "broken_links": 1,
        "celery_group_id": mock.ANY,
        "external_links": 0,
        "headings": {'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0},
        "html_version": 'html5',
        "id": mock.ANY,
        "internal_links": 2,
        "may_contain_login_form": False,
        "original_url": 'https://example.com',
        "state": COMPLETED,
        "status_code": 200,
        "title": ''
    }
