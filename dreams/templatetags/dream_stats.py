from django import template
from django.utils import timezone

from collections import Counter

register = template.Library()

@register.simple_tag(takes_context=True)
def total_dreams(context):
    return len(context["user"].dream_set.all())

@register.simple_tag(takes_context=True)
def weekly_dreams(context):
    now = timezone.now()
    start = now - timezone.timedelta(days=7)

    return len(context["user"].dream_set.filter(timestamp__gte=start, timestamp__lte=now))

@register.simple_tag(takes_context=True)
def most_common_theme(context, start, end=None):
    dream_list = context["user"].dream_set.filter(timestamp__gte=start.date(), timestamp__lte=(end.date() if end else start.date()))
    themes = list()

    for dream in dream_list:
        for theme in dream.dreamtheme_set.all():
            themes.append(theme.theme)

    try:
        most_common = Counter(themes).most_common(1)[0]
        return most_common[0], most_common[1]
    except:
        return None, None

@register.simple_tag(takes_context=True)
def most_common_theme_weekly(context):
    now = timezone.now()
    start = now - timezone.timedelta(days=7)

    return most_common_theme(context, start, now)

@register.simple_tag(takes_context=True)
def special_dreams(context, start, end=None):
    dream_list = context["user"].dream_set.filter(timestamp__gte=start.date(), timestamp__lte=(end.date() if end else start.date()))
    wet = 0
    lucid = 0

    for dream in dream_list:
        if dream.lucid:
            lucid += 1
        if dream.wet:
            wet += 1

    return lucid, wet

@register.simple_tag(takes_context=True)
def special_dreams_weekly(context):
    now = timezone.now()
    start = now - timezone.timedelta(days=7)

    return special_dreams(context, start, now)