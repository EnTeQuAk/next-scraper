import os
import os.path

import pytest
import responses

from django.conf import settings as django_settings


def pytest_configure(config):
    if not django_settings.configured:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "next_scraper.conf.test")

    # override a few things with our test specifics
    django_settings.INSTALLED_APPS = tuple(django_settings.INSTALLED_APPS) + (
        "next_scraper.tests",
    )


@pytest.fixture(autouse=True)
def start_responses_mocking(request):
    """Enable ``responses`` this enforcing us to explicitly mark tests
    that require internet usage.
    """
    marker = request.node.get_closest_marker('allow_external_http_requests')

    if not marker:
        responses.start()

    yield

    try:
        if not marker:
            responses.stop()
            responses.reset()
    except RuntimeError:
        # responses patcher was already uninstalled
        pass
