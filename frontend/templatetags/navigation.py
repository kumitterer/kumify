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
            try:
                sections += features.NAV_SECTIONS
            except:
                pass
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
    """ + section.get_html() for section in sections