from frontend.classes import NavSection, NavItem

from django.urls import reverse_lazy

dreams_section = NavSection("Dreams")

dreams_items = {
    "dreams_dream_list": NavItem("Dream List", reverse_lazy("dreams:dream_list")),
    "dreams_theme_list": NavItem("Themes", reverse_lazy("dreams:theme_list")),
    "dreams_notification_list": NavItem("Notifications", reverse_lazy("dreams:notification_list"))
}

for _, item in dreams_items.items():
    dreams_section.add_item(item)

NAV_SECTIONS = [dreams_section]