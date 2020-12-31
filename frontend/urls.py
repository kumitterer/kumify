from .views import DashboardView, UserRegistrationView

from django.urls import path, include

app_name = "frontend"

urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('accounts/register/', UserRegistrationView.as_view(), name="register"),
]
