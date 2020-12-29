from .views import StatusListView, StatusViewView, StatusDeleteView, StatusEditView, StatusCreateView, ActivityListView, ActivityEditView, ActivityCreateView, ActivityDeleteView, MoodListView, MoodEditView, NotificationCreateView, NotificationDeleteView, NotificationEditView, NotificationListView

from django.urls import path, include

app_name = "mood"

urlpatterns = [
    path('', StatusListView.as_view(), name="status_list"),
    path('status/<int:id>/view/', StatusViewView.as_view(), name="status_view"),
    path('status/<int:id>/edit/', StatusEditView.as_view(), name="status_edit"),
    path('status/<int:id>/delete/', StatusDeleteView.as_view(), name="status_delete"),
    path('status/new/', StatusCreateView.as_view(), name="status_create"),
    path('activity/', ActivityListView.as_view(), name="activity_list"),
    path('activity/<int:id>/edit/', ActivityEditView.as_view(), name="activity_edit"),
    path('activity/new/', ActivityCreateView.as_view(), name="activity_create"),
    path('activity/<int:id>/delete/', ActivityDeleteView.as_view(), name="activity_delete"),
    path('mood/', MoodListView.as_view(), name="mood_list"),
    path('mood/<int:id>/edit/', MoodEditView.as_view(), name="mood_edit"),
    path('notification/', NotificationListView.as_view(), name="notification_list"),
    path('notification/<int:id>/edit/', NotificationEditView.as_view(), name="notification_edit"),
    path('notification/<int:id>/delete/', NotificationDeleteView.as_view(), name="notification_delete"),
    path('notification/new/', NotificationCreateView.as_view(), name="notification_create"),
]