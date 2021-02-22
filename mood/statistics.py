import holoviews as hv
import pandas as pd

from django.utils import timezone

from bokeh.models import HoverTool
from holoviews.operation import timeseries
from dateutil.relativedelta import relativedelta

from .models import Status, Mood

def moodstats(user, mindate=None, maxdate=None, days=7):
    hv.extension('bokeh')

    maxdate = maxdate or timezone.now()
    mindate = mindate or (maxdate - relativedelta(days=days))

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
        width=600, height=400, show_grid=True,
        title='Your Mood Entries')

    pointtuples = [(pointdict["date"][i], pointdict["value"][i]) for i in range(len(pointdict["date"]))]

    line = hv.Curve(pointtuples)

    maxval = Mood.objects.filter(user=user).latest("value").value
    maxy = maxval + min(maxval * 0.1, 1)

    maxx = maxdate.timestamp() * 1000
    minx = maxx - (60*60*24*7) * 1000

    output = points * line * timeseries.rolling(line, rolling_window=7)
    output.opts(ylim=(0, maxy), xlim=(minx, maxx))

    return output

def activitystats(user, mindate=None, maxdate=None, days=7):
    maxdate = maxdate or timezone.now()
    mindate = mindate or (maxdate - relativedelta(days=days))

    output = {}

    for status in Status.objects.filter(user=user, timestamp__gte=mindate, timestamp__lte=maxdate):
        for activity in status.activity_set:
            if activity in output.keys():
                output[activity] += 1
            else:
                output[activity] = 1

    return output