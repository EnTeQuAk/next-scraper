from rest_framework import renderers


class JSONRenderer(renderers.JSONRenderer):
    media_type = "application/vnd.next_scraper+json"
