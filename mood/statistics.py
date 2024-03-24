import holoviews as hv
import pandas as pd

from django.utils import timezone

from math import pi

from bokeh.models import HoverTool
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.layouts import row, column
from holoviews.operation import timeseries
from dateutil.relativedelta import relativedelta

from .models import Status, Mood, StatusActivity

def moodstats(user):
    hv.extension('bokeh')

    tooltips = [
    ('Date', '@date{%F %H:%M}'),
    ('Mood', '@name (@value)')
    ]

    formatters = {
        '@date': 'datetime'
    }

    hover = HoverTool(tooltips=tooltips, formatters=formatters)

    pointdict = {"date": [], "value": [], "color": [], "name": []}


    for status in Status.objects.filter(user=user):
        if status.mood:
            pointdict["date"].append(status.timestamp)
            pointdict["value"].append(status.mood.value)
            pointdict["color"].append(status.mood.color)
            pointdict["name"].append(status.mood.name)

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

def moodpies(user):
    hv.extension('bokeh')

    maxdate = timezone.now()

    weekly_moods = Status.objects.filter(user=user, timestamp__lte=maxdate, timestamp__gte=maxdate - relativedelta(weeks=1))
    monthly_moods = Status.objects.filter(user=user, timestamp__lte=maxdate, timestamp__gte=maxdate - relativedelta(months=1))
    yearly_moods = Status.objects.filter(user=user, timestamp__lte=maxdate, timestamp__gte=maxdate - relativedelta(years=1))

    weekly = dict()
    colors = []

    for mood in Mood.objects.filter(user=user):
        weekly[mood.name] = 0
        colors.append(mood.color)

    monthly, yearly = weekly.copy(), weekly.copy()

    for status in weekly_moods:
        if status.mood:
            weekly[status.mood.name] += 1

    for status in monthly_moods:
        if status.mood:
            monthly[status.mood.name] += 1

    for status in yearly_moods:
        if status.mood:
            yearly[status.mood.name] += 1

    weekly_data = pd.Series(weekly).reset_index(name='value').rename(columns={'index':'mood'})
    weekly_data['angle'] = weekly_data['value']/weekly_data['value'].sum() * 2*pi
    weekly_data['color'] = colors

    weekly_chart = figure(height=350, title="Weekly", toolbar_location=None,
            tools="hover", tooltips="@mood: @value")
    weekly_chart.axis.visible = False

    weekly_chart.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='mood', source=weekly_data)

    monthly_data = pd.Series(monthly).reset_index(name='value').rename(columns={'index':'mood'})
    monthly_data['angle'] = monthly_data['value']/monthly_data['value'].sum() * 2*pi
    monthly_data['color'] = colors

    monthly_chart = figure(height=350, title="Monthly", toolbar_location=None,
            tools="hover", tooltips="@mood: @value")
    monthly_chart.axis.visible = False

    monthly_chart.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='mood', source=monthly_data)

    yearly_data = pd.Series(yearly).reset_index(name='value').rename(columns={'index':'mood'})
    yearly_data['angle'] = yearly_data['value']/yearly_data['value'].sum() * 2*pi
    yearly_data['color'] = colors

    yearly_chart = figure(height=350, title="Yearly", toolbar_location=None,
            tools="hover", tooltips="@mood: @value")
    yearly_chart.axis.visible = False

    yearly_chart.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='mood', source=yearly_data)

    return column(weekly_chart, monthly_chart, yearly_chart)

def activitymood(activity):
    hv.extension('bokeh')

    tooltips = [
    ('Date', '@date{%F %H:%M}'),
    ('Mood', '@name (@value)')
    ]

    formatters = {
        '@date': 'datetime'
    }

    hover = HoverTool(tooltips=tooltips, formatters=formatters)

    pointdict = {"date": [], "value": [], "color": [], "name": []}

    for statusactivity in StatusActivity.objects.filter(activity=activity):
        if statusactivity.status.mood:
            pointdict["date"].append(statusactivity.status.timestamp)
            pointdict["value"].append(statusactivity.status.mood.value)
            pointdict["color"].append(statusactivity.status.mood.color)
            pointdict["name"].append(statusactivity.status.mood.name)

    pointframe = pd.DataFrame.from_dict(pointdict)

    points = hv.Points(pointframe)

    points.opts(
        tools=[hover], color='color', cmap='Category20',
        line_color='black', size=25,
        width=600, height=400, show_grid=True)

    pointtuples = [(pointdict["date"][i], pointdict["value"][i]) for i in range(len(pointdict["date"]))]

    line = hv.Curve(pointtuples)

    maxval = Mood.objects.filter(user=activity.user).latest("value").value
    maxy = maxval + max(maxval * 0.1, 1)

    maxx = timezone.now().timestamp() * 1000
    minx = maxx - (60*60*24*7) * 1000

    output = points * line * timeseries.rolling(line, rolling_window=7)
    output.opts(ylim=(0, maxy), xlim=(minx, maxx))

    return output

def activitypies(activity):
    hv.extension('bokeh')

    maxdate = timezone.now()

    sa = StatusActivity.objects.filter(activity=activity)

    weekly = dict()
    colors = []

    for mood in Mood.objects.filter(user=activity.user):
        weekly[mood.name] = 0
        colors.append(mood.color)

    monthly, yearly = weekly.copy(), weekly.copy()

    for single in sa:
        if single.status.mood:
            if single.status.timestamp > timezone.now() - relativedelta(weeks=1):
                weekly[single.status.mood.name] += 1
            if single.status.timestamp > timezone.now() - relativedelta(months=1):
                monthly[single.status.mood.name] += 1
            if single.status.timestamp > timezone.now() - relativedelta(years=1):
                yearly[single.status.mood.name] += 1

    weekly_data = pd.Series(weekly).reset_index(name='value').rename(columns={'index':'mood'})
    weekly_data['angle'] = weekly_data['value']/weekly_data['value'].sum() * 2*pi
    weekly_data['color'] = colors

    weekly_chart = figure(height=350, title="Weekly", toolbar_location=None,
            tools="hover", tooltips="@mood: @value")
    weekly_chart.axis.visible = False

    weekly_chart.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='mood', source=weekly_data)

    monthly_data = pd.Series(monthly).reset_index(name='value').rename(columns={'index':'mood'})
    monthly_data['angle'] = monthly_data['value']/monthly_data['value'].sum() * 2*pi
    monthly_data['color'] = colors

    monthly_chart = figure(height=350, title="Monthly", toolbar_location=None,
            tools="hover", tooltips="@mood: @value")
    monthly_chart.axis.visible = False

    monthly_chart.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='mood', source=monthly_data)

    yearly_data = pd.Series(yearly).reset_index(name='value').rename(columns={'index':'mood'})
    yearly_data['angle'] = yearly_data['value']/yearly_data['value'].sum() * 2*pi
    yearly_data['color'] = colors

    yearly_chart = figure(height=350, title="Yearly", toolbar_location=None,
            tools="hover", tooltips="@mood: @value")
    yearly_chart.axis.visible = False

    yearly_chart.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='mood', source=yearly_data)

    return column(weekly_chart, monthly_chart, yearly_chart)