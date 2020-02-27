from django.urls import path
from rest_framework import routers

from .endpoints.scraper import ReportViewSet, StartScrapeView

router = routers.SimpleRouter()
router.register(r"report", ReportViewSet)

urlpatterns = [
    path("start/", StartScrapeView.as_view(), name="start-scraper"),
]

urlpatterns += router.urls
