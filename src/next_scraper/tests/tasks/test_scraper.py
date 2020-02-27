import pytest
import responses
from next_scraper.models import COMPLETED, NEW, Report
from next_scraper.tasks.scraper import (extract_information_from_page,
                                        fetch_status_from_links,
                                        mark_report_as_completed)


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
def test_fetch_status_from_links():
    report = Report.objects.create(original_url='https://example.com')

    fetch_status_from_links(
        ['https://example.com/broken', 'https://example.com/success'],
        report.pk)

    report.refresh_from_db()
    assert report.broken_links == 1


@pytest.mark.django_db
def test_report_as_completed():
    report = Report.objects.create(original_url='https://example.com', state=NEW)

    mark_report_as_completed(report.pk)

    report.refresh_from_db()
    assert report.state == COMPLETED


@pytest.mark.django_db
def test_extract_information_from_page_basics():
    report_pk = extract_information_from_page('https://example.com')

    report = Report.objects.get(pk=report_pk)

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
def test_extract_information_from_page_headings():
    responses.add(
        responses.GET,
        'https://headings.com',
        content_type='text/html',
        body='<!doctype html><html><h1>foo</h1><h3>bar</h3>'
    )

    report_pk = extract_information_from_page('https://headings.com')

    report = Report.objects.get(pk=report_pk)

    assert report.state == COMPLETED
    assert report.status_code == 200
    assert report.headings == {
        "h1": 1,
        "h2": 0,
        "h3": 1,
        "h4": 0,
        "h5": 0,
        "h6": 0
    }


@pytest.mark.django_db
def test_extract_information_from_page_title():
    responses.add(
        responses.GET,
        'https://title.com',
        content_type='text/html',
        body='<!doctype html><html><head><title>Page title</title></head>'
    )

    report_pk = extract_information_from_page('https://title.com')

    report = Report.objects.get(pk=report_pk)

    assert report.state == COMPLETED
    assert report.status_code == 200
    assert report.title == 'Page title'


@pytest.mark.django_db
def test_extract_information_from_login_form():
    responses.add(
        responses.GET,
        'https://login.com',
        content_type='text/html',
        body='<!doctype html><html><form><input type=text></form>'
    )

    report_pk = extract_information_from_page('https://login.com')

    report = Report.objects.get(pk=report_pk)

    assert report.state == COMPLETED
    assert report.status_code == 200
    assert report.may_contain_login_form
