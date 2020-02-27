from urllib.parse import urljoin, urlparse

import requests
from celery import group
from django.db.models import F
from lxml import html
from more_itertools import chunked
from rest_framework.status import is_success

from ..models import COMPLETED, RUNNING, Report
from ..utils.html import get_html_version_from_tree, pick_possible_login_form
from . import task


def _create_chunked_task_signatures(
    task, items, chunk_size, task_args=None, task_kwargs=None
):
    """
    Splits a task depending on a list of items into a bunch of tasks of the
    specified chunk_size, passing a chunked queryset and optional additional
    arguments to each.

    Return the group of task signatures without executing it."""
    if task_args is None:
        task_args = ()
    if task_kwargs is None:
        task_kwargs = {}

    return group(
        [
            task.si(chunk, *task_args, **task_kwargs)
            for chunk in chunked(items, chunk_size)
        ]
    )


@task
def fetch_status_from_links(urls, report_pk):
    report = Report.objects.get(pk=report_pk)

    for url in urls:
        full_url = urljoin(report.original_url, url)
        response = requests.get(full_url)

        if not is_success(response.status_code):
            Report.objects.filter(pk=report_pk).update(
                broken_links=F("broken_links") + 1
            )


@task
def mark_report_as_completed(report_pk):
    report = Report.objects.get(pk=report_pk)
    report.state = COMPLETED

    report.save(update_fields=("state",))


@task
def extract_information_from_page(page_url):
    report = Report.objects.create(original_url=page_url)

    # Mark the report as running as we're going to start evaluating the page
    report.state = RUNNING
    report.save(update_fields=("state",))

    response = requests.get(page_url)

    report.status_code = response.status_code
    report.save(update_fields=("status_code",))

    if not is_success(response.status_code):
        report.state = COMPLETED
        report.save(update_fields=("state",))
        return report.pk

    tree = html.fromstring(response.content)
    links = [
        link
        for link in tree.xpath("//a/@href")
        if not link.startswith("#")
        and link not in ("javascript:;", "javascript:void(0)")
    ]

    # Now let's start fetching broken links from the page in the background
    # so that it completes as soon as possible and runs while we do more
    # analysis on the page.
    # Note that from this point on we *have to use* update_fields=() to
    # avoid overwriting the `broken_links` counter in the middle of analysis
    fetch_broken_links_tasks = _create_chunked_task_signatures(
        task=fetch_status_from_links,
        items=list(links),
        chunk_size=25,
        task_args=(report.pk,),
    )

    # Force the group to be assigned a group_id ahead of creating the chord
    # in the next step. This will allow us to track the group separately
    # and implement proper progress-stats.
    # Running .save() will save it into the result backend and keep it there.
    group_result = fetch_broken_links_tasks.freeze()
    group_result.save()

    # Save the group id for better tracking of completed status_code
    report.celery_group_id = group_result.id
    report.save(update_fields=("celery_group_id",))

    workflow = fetch_broken_links_tasks | mark_report_as_completed.si(report.pk)

    # Fire it up.
    workflow.apply_async()

    # While the links get fetched we can analyze the actual page more.
    # This may be put into a separate helper method but let's keep it here
    # for now till it grows too big.
    # Note that this doesn't properly take subdomains into account yet.
    base_domain = urlparse(page_url).netloc
    report.external_links = len(
        [x for x in links if urlparse(x).netloc and urlparse(x).netloc != base_domain]
    )
    report.internal_links = len(
        [
            x
            for x in links
            if urlparse(x).netloc == "" or urlparse(x).netloc == base_domain
        ]
    )

    login_form = pick_possible_login_form(tree.xpath("//form"))
    report.may_contain_login_form = login_form is not None

    report.html_version = get_html_version_from_tree(tree)
    report.title = tree.xpath("string(//title)")
    report.headings = {
        # We need to cast to int() here as count() returns a float
        # but we really just want integer numbers.
        "h1": int(tree.xpath("count(//h1)")),
        "h2": int(tree.xpath("count(//h2)")),
        "h3": int(tree.xpath("count(//h3)")),
        "h4": int(tree.xpath("count(//h4)")),
        "h5": int(tree.xpath("count(//h5)")),
        "h6": int(tree.xpath("count(//h6)")),
    }

    report.save(
        update_fields=(
            "external_links",
            "internal_links",
            "may_contain_login_form",
            "html_version",
            "title",
            "headings",
        )
    )

    return report.pk
