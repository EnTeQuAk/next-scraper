import urllib
from urllib.parse import urlencode, urljoin

import pkg_resources
import requests


class APIError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"<APIError({self.message})>"


class Client(requests.Session):
    """Proof of concept client implementation."""
    content_type = "application/vnd.next_scraper+json"

    host = "scrapy.io"
    port = "80"
    timeout = 3.0

    def build_url(self, endpoint, qs=None):
        url = urljoin(f"http://{self.host}:{self.port}", endpoint)

        if qs:
            url += "?" + urlencode(qs)
        return url

    def request(self, method, url, *args, **kwargs):
        parse_result = urllib.parse.urlparse(url)

        dist = pkg_resources.get_distribution("next_scraper")

        headers = {
            "User-Agent": f"Next Scraper {dist.version}",
            "Host": parse_result.netloc,
            "Method": method,
            "Path": parse_result.path,
            "Accept": self.content_type,
            "Content-Type": self.content_type,
        }

        headers.update(kwargs.pop("headers", {}))

        kwargs.update({"headers": headers, "timeout": self.timeout})

        return super(Client, self).request(method, url, *args, **kwargs)

    def _api_request(self, method, *args, **kwargs):
        try:
            response = self.request(method, *args, **kwargs)
        except requests.HTTPError as exc:
            msg = "lalalal"

            if msg:
                raise APIError(msg)
            else:
                raise exc

        return response

    def scrape_url(self, url):
        url = self.build_url("/scraper/start/")
        response = self._api_request("POST", url)

        if response.status_code == 400:
            raise APIError(response.content.decode())

        assert response.status_code == 201
        return response


class LocalClient(Client):
    host = "localhost"
    port = "8000"
    force_https = False
