from .views import CronHandlerView

from django.urls import path

app_name = "cron"

urlpatterns = [
    path('', CronHandlerView.as_view(), name="cronhandler"),
]