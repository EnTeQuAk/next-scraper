import json

from rest_framework.test import APIClient as BaseAPIClient


class APIClient(BaseAPIClient):
    """
    Subclass to handle our custom accept headers required
    for proper versioning and data parsing.
    """

    content_type = "application/vnd.next_scraper+json"
    default_format = "json"

    def generic(self, method, path, data="", content_type=None, secure=False, **extra):
        extra.update({"HTTP_HOST": "testserver", "HTTP_ACCEPT": self.content_type})

        return super().generic(method, path, data, self.content_type, secure, **extra)

    def _parse_json(self, response, **extra):
        content_type = response.get("Content-Type")
        types = ("application/json", self.content_type)

        if not any(type in content_type for type in types):
            raise ValueError(
                f'Content-Type header is "{content_type}", ' f'not "application/json"'
            )

        return json.loads(response.content.decode(), **extra)
