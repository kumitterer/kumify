from .views import GPSLogView

from django.urls import path

app_name = "gpslog"

urlpatterns = [
    path('<uuid:track>/<uuid:token>/', GPSLogView.as_view(), name="gpslog"),
]