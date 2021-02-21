import holoviews as hv
import pandas as pd

from django.utils import timezone

from bokeh.models import HoverTool
from dateutil.relativedelta import relativedelta

from .models import Status

def moodstats(mindate=None, maxdate=None, days=7):
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

    for status in Status.objects.filter(timestamp__gte=mindate, timestamp__lte=maxdate):
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

    output = points * line
    output.opts(tools=["xwheel_zoom"])

    return output