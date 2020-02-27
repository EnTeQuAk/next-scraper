import pytest
from urllib3.util.url import parse_url

from next_scraper.client import LocalClient


@pytest.mark.django_db(transaction=True)
class TestTestClient:
    @pytest.fixture(autouse=True)
    def setup(self, settings, live_server):
        self.liveserver = live_server

    def get_client(self, jwt_token=None):
        client = LocalClient(jwt_token)
        parsed_url = parse_url(self.liveserver.url)
        client.host = parsed_url.host
        client.port = parsed_url.port
        return client
