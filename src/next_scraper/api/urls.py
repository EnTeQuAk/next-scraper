from django.urls import path

from .endpoints.scraper import StartUrlScrape


urlpatterns = [
    path("scraper/start/", StartUrlScrape.as_view(), name="start-scraper"),
]
