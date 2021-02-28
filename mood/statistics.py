import holoviews as hv
import pandas as pd

from django.utils import timezone

from bokeh.models import HoverTool
from holoviews.operation import timeseries
from dateutil.relativedelta import relativedelta

from .models import Status, Mood

def moodstats(user):
    hv.extension('bokeh')

    tooltips = [
    ('Date', '@date{%F %H:%M}'),
    ('Value', '@value')
    ]

    formatters = {
        '@date': 'datetime'
    }

    hover = HoverTool(tooltips=tooltips, formatters=formatters)

    pointdict = {"date": [], "value": [], "color": []}


    for status in Status.objects.filter(user=user):
        if status.mood:
            pointdict["date"].append(status.timestamp)
            pointdict["value"].append(status.mood.value)
            pointdict["color"].append(status.mood.color)

    pointframe = pd.DataFrame.from_dict(pointdict)

    points = hv.Points(pointframe)

    points.opts(
        tools=[hover], color='color', cmap='Category20',
        line_color='black', size=25,
        width=600, height=400, show_grid=True)

    pointtuples = [(pointdict["date"][i], pointdict["value"][i]) for i in range(len(pointdict["date"]))]

    line = hv.Curve(pointtuples)

    maxval = Mood.objects.filter(user=user).latest("value").value
    maxy = maxval + max(maxval * 0.1, 1)

    maxx = timezone.now().timestamp() * 1000
    minx = maxx - (60*60*24*7) * 1000

    output = points * line * timeseries.rolling(line, rolling_window=7)
    output.opts(ylim=(0, maxy), xlim=(minx, maxx))

    return output

def activitystats(user):
    output = {}

    for status in Status.objects.filter(user=user):
        for activity in status.activity_set:
            if not activity in output.keys():
                output[activity] = {
                    "alltime": 0,
                    "yearly": 0,
                    "monthly": 0,
                    "weekly": 0
                }

            output[activity]["alltime"] += 1

            if status.timestamp > timezone.now() - relativedelta(years=1):
                output[activity]["yearly"] += 1

            if status.timestamp > timezone.now() - relativedelta(months=1):
                output[activity]["monthly"] += 1

            if status.timestamp > timezone.now() - relativedelta(weeks=1):
                output[activity]["weekly"] += 1

    return output