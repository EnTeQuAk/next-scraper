import pytest
import responses


def pytest_configure(config):
    import django
    # Forcefully call `django.setup`, pytest-django tries to be very lazy
    # and doesn't call it if it has already been setup.
    # That is problematic for us since we overwrite our logging config
    # in settings_test and it can happen that django get's initialized
    # with the wrong configuration. So let's forcefully re-initialize
    # to setup the correct logging config since at this point
    # DJANGO_SETTINGS_MODULE should be `next_scraper.conf.test` every time.
    django.setup()


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
