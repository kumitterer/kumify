from frontend.classes import NavSection, NavItem

from django.urls import reverse_lazy

mood_section = NavSection("Mood")

mood_items = {
    "mood_status_list": NavItem("Status List", reverse_lazy("mood:status_list")),
    "mood_activity_list": NavItem("Activities", reverse_lazy("mood:activity_list")),
    "mood_mood_list": NavItem("Moods", reverse_lazy("mood:mood_list")),
    "mood_notification_list": NavItem("Notifications", reverse_lazy("mood:notification_list")),
    "mood_statistics": NavItem("Statistics", reverse_lazy("mood:statistics"))
}

for _, item in mood_items.items():
    mood_section.add_item(item)

NAV_SECTIONS = [mood_section]