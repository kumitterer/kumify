from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def querystring(context, **kwargs):
    string = context["request"].GET.urlencode()
    return f"?{string}" if string else ""