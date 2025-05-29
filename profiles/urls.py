from django.urls import path
from .views import UserProfileView, UserProfileEditView

app_name = "profiles"

urlpatterns = [
    path('', UserProfileView.as_view(), name="profile_view"),
    path('edit/', UserProfileEditView.as_view(), name="profile_edit"),
]