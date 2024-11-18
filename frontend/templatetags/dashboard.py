from django import template
from django.conf import settings

from importlib import import_module

register = template.Library()


@register.simple_tag(takes_context=True)
def dashboard(context):
    sections = []

    for module in settings.CORE_MODULES + settings.ENABLED_MODULES:
        try:
            features = import_module(f"{module}.features")
            try:
                sections += features.DASHBOARD_SECTIONS
            except Exception:
                pass
        except Exception:
            pass

    dashboard_html = ""

    for section in sections:
        dashboard_html += f"<h2>{section.name}</h2>"

        dashboard_html += section.get_html(context["request"])

        if section != sections[-1]:
            dashboard_html += '<hr class="dashboard-divider">'

    return dashboard_html
