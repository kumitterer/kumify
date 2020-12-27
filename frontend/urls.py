from .views import DashboardView

from django.urls import path, include

app_name = "frontend"

urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
]
