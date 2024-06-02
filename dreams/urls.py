from .views import DreamListView, DreamViewView, DreamDeleteView, DreamEditView, DreamCreateView, ThemeListView, ThemeEditView, ThemeCreateView, ThemeDeleteView, NotificationCreateView, NotificationDeleteView, NotificationEditView, NotificationListView

from django.urls import path

app_name = "dreams"

urlpatterns = [
    path('', DreamListView.as_view(), name="dream_list"),
    path('dream/<int:id>/view/', DreamViewView.as_view(), name="dream_view"),
    path('dream/<int:id>/edit/', DreamEditView.as_view(), name="dream_edit"),
    path('dream/<int:id>/delete/', DreamDeleteView.as_view(), name="dream_delete"),
    path('dream/new/', DreamCreateView.as_view(), name="dream_create"),
    path('theme/', ThemeListView.as_view(), name="theme_list"),
    path('theme/<int:id>/edit/', ThemeEditView.as_view(), name="theme_edit"),
    path('theme/new/', ThemeCreateView.as_view(), name="theme_create"),
    path('theme/<int:id>/delete/', ThemeDeleteView.as_view(), name="theme_delete"),
    path('notification/', NotificationListView.as_view(), name="notification_list"),
    path('notification/<int:id>/edit/', NotificationEditView.as_view(), name="notification_edit"),
    path('notification/<int:id>/delete/', NotificationDeleteView.as_view(), name="notification_delete"),
    path('notification/new/', NotificationCreateView.as_view(), name="notification_create"),
]