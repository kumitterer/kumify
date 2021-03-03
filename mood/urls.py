from .views import StatusListView, StatusViewView, StatusDeleteView, StatusEditView, StatusCreateView, ActivityListView, ActivityEditView, ActivityCreateView, ActivityDeleteView, MoodListView, MoodEditView, NotificationCreateView, NotificationDeleteView, NotificationEditView, NotificationListView, MoodStatisticsView, MoodCSVView, MoodPlotView, MoodPiesView, ActivityStatisticsView, ActivityPlotView, ActivityPiesView

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
    path('statistics/', MoodStatisticsView.as_view(), name="statistics"),
    path('statistics/csv/', MoodCSVView.as_view(), name="statistics_csv"),
    path('statistics/plot/', MoodPlotView.as_view(), name="statistics_plot"),
    path('statistics/pies/', MoodPiesView.as_view(), name="statistics_pies"),
    path('statistics/activity/<int:id>/', ActivityStatisticsView.as_view(), name="statistics_activity"),
    path('statistics/activity/<int:id>/plot/', ActivityPlotView.as_view(), name="statistics_activity_plot"),
    path('statistics/activity/<int:id>/pies/', ActivityPiesView.as_view(), name="statistics_activity_pies"),
]