from rest_framework import generics, permissions, status, viewsets
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response

from next_scraper.api.serializers import ReportSerializer
from next_scraper.models import Report
from next_scraper.tasks.scraper import extract_information_from_page


class StartScrapeView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        url = request.data.get("url", None)

        # TODO: This probably better belongs into a serializer
        if url is None:
            return Response(
                {"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if Report.objects.filter(original_url=url).exists():
            return Response(
                {
                    "error": "Report already created. Do use /report/ to retrieve"
                    "the information stored for this report"
                },
                status=status.HTTP_409_CONFLICT,
            )

        extract_information_from_page.delay(url)

        return Response(status=status.HTTP_201_CREATED)


class ReportViewSet(RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    lookup_field = "original_url"
    lookup_url_kwarg = "url"
    # Let's not go down the route of validating URLs properly for now
    # we can do that when we have too much time :)
    lookup_value_regex = ".+"
