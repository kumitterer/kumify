from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.gis.geos import Point

from .models import GPSTrack, GPSToken


class GPSLogView(LoginRequiredMixin, View):
    # TODO: Finish this view
    def dispatch(self, request, *args, **kwargs):
        self.gps_track = get_object_or_404(GPSTrack, id=self.kwargs["track"])
        self.gps_token = get_object_or_404(
            GPSToken, track=self.gps_track, token=self.kwargs["token"])

        if request.method == "POST" and not self.gps_token.write:
            return self.http_method_not_allowed(request, *args, **kwargs)

        return super().dispatch(request, *args, **kwargs)

# ?lat=47.07047834&lon=15.45140181&alt=427.04833984375&tst=1043419092&batt=23.0&acc=14.692631721496582&spd=0.0&dir=&sat=6

    def get(self, request, *args, **kwargs):
        if self.gps_token.write and all(field in request.GET for field in ("lat", "lon")):
            lat = request.GET["lat"]
            lon = request.GET["lon"]

            alt = request.GET.get("alt", None)

            point = Point(lat, lon, alt)  # noqa: F841

            tst = request.GET.get("tst", timezone.now().timestamp())  # noqa: F841

    def post(self, request, *args, **kwargs):
        pass
