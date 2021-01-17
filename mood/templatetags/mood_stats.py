from django import template
from django.utils import timezone

from collections import Counter

register = template.Library()

@register.simple_tag(takes_context=True)
def total_moods(context):
    return len(context["user"].status_set.all())

@register.simple_tag(takes_context=True)
def current_streak(context):
    status_list = context["user"].status_set.all().order_by("-timestamp")
    timestamp = None
    counter = 0

    for status in status_list:
        if not timestamp:
            if not (status.timestamp.date() == timezone.now().date() or status.timestamp.date() == (timezone.now() - timezone.timedelta(days=1)).date()):
                return counter
            timestamp = status.timestamp
            counter += 1
            continue

        if status.timestamp.date() == timestamp.date():
            continue

        if status.timestamp.date() == timestamp.date() - timezone.timedelta(days=1):
            timestamp = status.timestamp
            counter += 1
            continue

        return counter        

@register.simple_tag(takes_context=True)
def closest_mood(context, value):
    mood_list = context["user"].mood_set.all()

    found = None

    for mood in mood_list:
        if (not found) or (abs(mood.value - value) < abs(found.value - value)):
            found = mood

    return found

@register.simple_tag(takes_context=True)
def average_mood(context, start, end=None, daily_averages=True):
    status_list = context["user"].status_set.filter(timestamp__gte=start.date(), timestamp__lte=(end.date() if end else start.date()))
    moods = list() if not daily_averages else dict()

    for status in status_list:
        if status.mood:
            if daily_averages:
                if not status.timestamp.date() in moods.keys():
                    moods[status.timestamp.date()] = [status.mood.value]
                else:
                    moods[status.timestamp.date()].append(status.mood.value)
            else:
                moods.append(status.mood.value)

    if daily_averages:
        moods = [sum(entries) / len(entries) for date, entries in moods.items()]

    try:
        average = sum(moods) / len(moods)
    except ZeroDivisionError:
        average = None

    return average

@register.simple_tag(takes_context=True)
def average_mood_weekly(context, daily_averages=True):
    now = timezone.now()
    start = now - timezone.timedelta(days=7)

    return average_mood(context, start, now, daily_averages)

@register.simple_tag(takes_context=True)
def most_common_activity(context, start, end=None):
    status_list = context["user"].status_set.filter(timestamp__gte=start.date(), timestamp__lte=(end.date() if end else start.date()))
    activities = list()

    for status in status_list:
        for activity in status.statusactivity_set.all():
            activities.append(activity.activity)

    most_common = Counter(activities).most_common(1)[0]

    return most_common[0], most_common[1]

@register.simple_tag(takes_context=True)
def most_common_activity_weekly(context):
    now = timezone.now()
    start = now - timezone.timedelta(days=7)

    return most_common_activity(context, start, now)