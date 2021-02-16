from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def other_activities(context):
    return context["user"].activity_set.filter(category=None)
