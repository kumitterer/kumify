from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def use_oidc():
    return settings.USE_OIDC

@register.simple_tag
def oidc_provider():
    return settings.OIDC_PROVIDER_NAME