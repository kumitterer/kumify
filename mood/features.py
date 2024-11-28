from frontend.classes import NavSection, NavItem, NavCollapse, DashboardSection

from django.urls import reverse_lazy
from django.templatetags.static import static

# Sidebar navigation items

mood_section = NavSection("Mood")

mood_settings_collapse = NavCollapse("Settings", icon="fas fa-fw fa-cog")

mood_status_list = NavItem("Status List", reverse_lazy("mood:status_list"))

mood_settings = [
    NavItem("Activities", reverse_lazy("mood:activity_list")),
    NavItem("Moods", reverse_lazy("mood:mood_list")),
    NavItem(
        "Notifications", reverse_lazy("mood:notification_list")
    ),
    NavItem("Statistics", reverse_lazy("mood:statistics")),
]

for setting in mood_settings:
    mood_settings_collapse.add_item(setting)

mood_section.add_item(mood_status_list)
mood_section.add_item(mood_settings_collapse)

NAV_SECTIONS = [mood_section]

# Dashboard sections

mood_section = DashboardSection("Moods", "mood/dashboard_section.html")

mood_section.add_script(static("mood/dist/js/d3.v7.min.js"))
mood_section.add_script(static("mood/dist/js/cal-heatmap.min.js"))
mood_section.add_script(static("mood/dist/js/popper.min.mjs"))
mood_section.add_script(static("mood/dist/js/Tooltip.min.js"))

mood_section.add_script(static("mood/dashboard.js"))

mood_section.add_style(static("mood/dist/css/cal-heatmap.css"))


DASHBOARD_SECTIONS = [mood_section]
