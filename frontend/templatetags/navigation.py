from django import template
from django.conf import settings

from importlib import import_module

register = template.Library()

@register.simple_tag
def sidebar_nav():
    sections = []

    for module in settings.CORE_MODULES + settings.ENABLED_MODULES:
        try:
            features = import_module(f"{module}.features")
        except:
            pass

    return """
            <li class="nav-item {% if title == "Dashboard" %}active{% endif %}">
                <a class="nav-link" href="{% url "frontend:dashboard" %}">
                    <i class="fas fa-fw fa-tachometer-alt"></i>
                    <span>Dashboard</span></a>
            </li>

            <!-- Divider -->
            <hr class="sidebar-divider">

            <!-- Heading -->
            <div class="sidebar-heading">
                Mood
            </div>

            <!-- Nav Item - Status List -->
            <li class="nav-item {% if title == "Status List" %}active{% endif %}">
                <a class="nav-link" href="{% url "mood:status_list" %}">
                    <i class="fas fa-fw fa-smile"></i>
                    <span>Status List</span></a>
            </li>

            <!-- Nav Item - Activity List -->
            <li class="nav-item {% if title == "Activities" %}active{% endif %}">
                <a class="nav-link" href="{% url "mood:activity_list" %}">
                    <i class="fas fa-fw fa-smile"></i>
                    <span>Activities</span></a>
            </li>

            <!-- Nav Item - Mood List -->
            <li class="nav-item {% if title == "Moods" %}active{% endif %}">
                <a class="nav-link" href="{% url "mood:mood_list" %}">
                    <i class="fas fa-fw fa-smile"></i>
                    <span>Moods</span></a>
            </li>

            <!-- Nav Item - Notification List -->
            <li class="nav-item {% if title == "Notifications" %}active{% endif %}">
                <a class="nav-link" href="{% url "mood:notification_list" %}">
                    <i class="fas fa-fw fa-smile"></i>
                    <span>Notifications</span></a>
            </li>

            <!-- Nav Item - Notification List -->
            <li class="nav-item {% if title == "Statistics" %}active{% endif %}">
                <a class="nav-link" href="{% url "mood:statistics" %}">
                    <i class="fas fa-fw fa-smile"></i>
                    <span>Statistics</span></a>
            </li>

            <!-- Divider -->
            <hr class="sidebar-divider">

            <!-- Heading -->
            <div class="sidebar-heading">
                Dreams
            </div>

            <!-- Nav Item - Dream List -->
            <li class="nav-item {% if title == "Dream List" %}active{% endif %}">
                <a class="nav-link" href="{% url "dreams:dream_list" %}">
                    <i class="fas fa-fw fa-smile"></i>
                    <span>Dream List</span></a>
            </li>

            <!-- Nav Item - Theme List -->
            <li class="nav-item {% if title == "Themes" %}active{% endif %}">
                <a class="nav-link" href="{% url "dreams:theme_list" %}">
                    <i class="fas fa-fw fa-smile"></i>
                    <span>Themes</span></a>
            </li>

            <!-- Nav Item - Notification List -->
            <li class="nav-item {% if title == "Notifications" %}active{% endif %}">
                <a class="nav-link" href="{% url "dreams:notification_list" %}">
                    <i class="fas fa-fw fa-smile"></i>
                    <span>Notifications</span></a>
            </li>
    """