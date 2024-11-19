from django import template
from django.conf import settings
from django.urls import reverse_lazy

from ..classes import NavSection

from importlib import import_module

register = template.Library()

@register.simple_tag
def sidebar_nav():
    sections: list[NavSection] = []

    for module in settings.CORE_MODULES + settings.ENABLED_MODULES:
        try:
            features = import_module(f"{module}.features")
            try:
                sections += features.NAV_SECTIONS
            except Exception:
                pass
        except Exception:
            pass

    return """
            <li class="nav-item">
                <a class="nav-link" href=\"""" +  reverse_lazy("frontend:dashboard") + """\">
                    <i class="fas fa-fw fa-tachometer-alt"></i>
                    <span>Dashboard</span></a>
            </li>

            <!-- Divider -->
            <hr class="sidebar-divider">
    """ + """
            <!-- Divider -->
            <hr class="sidebar-divider">
    """.join([section.get_html() for section in sections])