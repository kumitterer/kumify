from frontend.classes import NavSection, NavItem, NavCollapse, DashboardSection

from django.urls import reverse_lazy

# Sidebar navigation items

dreams_section = NavSection("Dreams")

dreams_settings_collapse = NavCollapse("Settings", icon="fas fa-fw fa-cog")

dream_list = NavItem("Dream List", reverse_lazy("dreams:dream_list"))

dreams_settings = [
    NavItem("Themes", reverse_lazy("dreams:theme_list")),
    NavItem("Notifications", reverse_lazy("dreams:notification_list")),
]

for item in dreams_settings:
    dreams_settings_collapse.add_item(item)

dreams_section.add_item(dream_list)
dreams_section.add_item(dreams_settings_collapse)

NAV_SECTIONS = [dreams_section]

# Dashboard sections

dreams_section = DashboardSection("Dreams", "dreams/dashboard_section.html")

DASHBOARD_SECTIONS = [dreams_section]
