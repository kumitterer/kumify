from django.views.generic import TemplateView, ListView, UpdateView, DetailView, CreateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.utils.decorators import method_decorator

from .models import Status, Activity, Mood, StatusMedia, StatusActivity
from .forms import StatusForm
from .statistics import moodstats, activitystats

from common.helpers import get_upload_path
from common.templatetags.images import hvhtml
from msgio.models import NotificationDailySchedule, Notification

from dateutil import relativedelta

from datetime import datetime

class StatusListView(LoginRequiredMixin, ListView):
    template_name = "mood/status_list.html"
    model = Status

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Status List"
        context["subtitle"] = "Just a list of your mood entries."
        context["buttons"] = [(reverse_lazy("mood:status_create"), "New Status", "plus")]
        return context

    def get_queryset(self):
        return Status.objects.filter(user=self.request.user).order_by('timestamp')


class StatusViewView(LoginRequiredMixin, DetailView):
    template_name = "mood/status_view.html"
    model = Status

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "View Status"
        context["subtitle"] = "View the details of your mood entry."
        context["buttons"] = [(reverse_lazy("mood:status_edit", kwargs={"id": self.kwargs["id"]}), "Edit Status", "pen")]
        return context

    def get_object(self):
        return get_object_or_404(Status, user=self.request.user, id=self.kwargs["id"])


class StatusCreateView(LoginRequiredMixin, CreateView):
    template_name = "mood/status_edit.html"
    form_class = StatusForm
    model = Status

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Status"
        context["subtitle"] = "How are you feeling today?"
        context["scripts"] = ["frontend/js/dropdown-to-buttons.js"]
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        ret = super().form_valid(form)

        for activity in form.cleaned_data["activities"]:
            if activity.user == self.request.user:
                StatusActivity.objects.create(activity=activity, status=form.instance)

        for attachment in form.cleaned_data["uploads"]:
            dba = StatusMedia(status=form.instance)
            dba.file.save(get_upload_path(form.instance, attachment.name), attachment)
            dba.save()

        return ret

    def get_success_url(self):
        return reverse_lazy("mood:status_view", kwargs={"id": self.object.id})


class StatusEditView(LoginRequiredMixin, UpdateView):
    template_name = "mood/status_edit.html"
    form_class = StatusForm
    model = Status

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Status"
        context["subtitle"] = "Change a status you created before."
        context["scripts"] = ["frontend/js/dropdown-to-buttons.js"]
        context["buttons"] = [(reverse_lazy("mood:status_delete", kwargs={"id": self.kwargs["id"]}), "Delete Status", "trash-alt")]
        return context

    def get_object(self):
        return get_object_or_404(Status, user=self.request.user, id=self.kwargs["id"])

    def form_valid(self, form):
        for attachment in form.cleaned_data["uploads"]:
            dba = StatusMedia(status=form.instance)
            dba.file.save(get_upload_path(form.instance, attachment.name), attachment)
            dba.save()
        
        for activity in form.cleaned_data["activities"]:
            if activity.user == self.request.user:
                if not activity in form.instance.activity_set:
                    StatusActivity.objects.create(activity=activity, status=form.instance)

        for statusactivity in form.instance.statusactivity_set.all():
            if not statusactivity.activity in form.cleaned_data["activities"]:
                statusactivity.delete()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mood:status_view", kwargs={"id": self.object.id})


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "mood/status_delete.html"
    model = Status

    def get_object(self):
        return get_object_or_404(Status, user=self.request.user, id=self.kwargs["id"])

    def get_success_url(self):
        return reverse_lazy("mood:status_list")


class ActivityListView(LoginRequiredMixin, ListView):
    template_name = "mood/activity_list.html"
    model = Activity

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Activities"
        context["subtitle"] = "The activities you have defined."
        context["buttons"] = [(reverse_lazy("mood:activity_create"), "Create Activity", "pen")]
        return context

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)


class ActivityEditView(LoginRequiredMixin, UpdateView):
    template_name = "mood/activity_edit.html"
    model = Activity
    fields = ["name", "icon", "color"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Activity"
        context["subtitle"] = "Make changes to the activity."
        context["scripts"] = ["colorfield/jscolor/jscolor.js", "colorfield/colorfield.js", "frontend/js/fontawesome-iconpicker.min.js", "frontend/js/iconpicker-loader.js"]
        context["styles"] = ["frontend/css/fontawesome-iconpicker.min.css"]
        context["buttons"] = [(reverse_lazy("mood:activity_delete", kwargs={"id": self.kwargs["id"]}), "Delete Activity", "trash-alt")]
        return context

    def get_object(self):
        return get_object_or_404(Activity, user=self.request.user, id=self.kwargs["id"])

    def get_success_url(self):
        return reverse_lazy("mood:activity_list")


class ActivityCreateView(LoginRequiredMixin, CreateView):
    template_name = "mood/activity_edit.html"
    model = Activity
    fields = ["name", "icon", "color"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Activity"
        context["subtitle"] = "Add a new activity."
        context["scripts"] = ["colorfield/jscolor/jscolor.js", "colorfield/colorfield.js", "frontend/js/fontawesome-iconpicker.min.js", "frontend/js/iconpicker-loader.js"]
        context["styles"] = ["frontend/css/fontawesome-iconpicker.min.css"]
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mood:activity_list")


class ActivityDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "mood/activity_delete.html"
    model = Activity

    def get_object(self):
        return get_object_or_404(Activity, user=self.request.user, id=self.kwargs["id"])

    def get_success_url(self):
        return reverse_lazy("mood:activity_list")


class MoodListView(LoginRequiredMixin, ListView):
    template_name = "mood/mood_list.html"
    model = Mood

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Moods"
        context["subtitle"] = "The different moods you have defined."
        return context

    def get_queryset(self):
        return Mood.objects.filter(user=self.request.user)


class MoodEditView(LoginRequiredMixin, UpdateView):
    template_name = "mood/mood_edit.html"
    model = Mood
    fields = ["name", "icon", "color", "value"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Mood"
        context["subtitle"] = "Make changes to the mood."
        context["scripts"] = ["colorfield/jscolor/jscolor.js", "colorfield/colorfield.js", "frontend/js/fontawesome-iconpicker.min.js", "frontend/js/iconpicker-loader.js"]
        context["styles"] = ["frontend/css/fontawesome-iconpicker.min.css"]
        return context

    def get_object(self):
        return get_object_or_404(Mood, user=self.request.user, id=self.kwargs["id"])

    def get_success_url(self):
        return reverse_lazy("mood:mood_list")


class MoodCreateView(LoginRequiredMixin, CreateView):
    template_name = "mood/mood_edit.html"
    model = Mood
    fields = ["name", "icon", "color", "value"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Activity"
        context["subtitle"] = "Add a new activity."
        context["scripts"] = ["colorfield/jscolor/jscolor.js", "colorfield/colorfield.js", "frontend/js/fontawesome-iconpicker.min.js", "frontend/js/iconpicker-loader.js"]
        context["styles"] = ["frontend/css/fontawesome-iconpicker.min.css"]
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mood:activity_list")


class NotificationListView(LoginRequiredMixin, ListView):
    template_name = "mood/notification_list.html"
    model = NotificationDailySchedule
    fields = ["time"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Notifications"
        context["subtitle"] = "The daily reminders you have set up."
        context["buttons"] = [(reverse_lazy("mood:notification_create"), "New Notification", "plus")]
        return context

    def get_queryset(self):
        return NotificationDailySchedule.objects.filter(notification__recipient=self.request.user, notification__app="mood")


class NotificationCreateView(LoginRequiredMixin, CreateView):
    template_name = "mood/notification_edit.html"
    model = NotificationDailySchedule
    fields = ["time"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Notification"
        context["subtitle"] = "Add a new daily notification."
        return context

    def form_valid(self, form):
        notification = Notification.objects.create(content="Hi, it's time for a new Kumify entry! Go to %KUMIFYURL% to document your mood!", recipient=self.request.user, app="mood")
        obj = form.save(commit=False)
        obj.notification = notification
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mood:notification_list")


class NotificationEditView(LoginRequiredMixin, UpdateView):
    template_name = "mood/notification_edit.html"
    model = NotificationDailySchedule
    fields = ["time"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Notification"
        context["subtitle"] = "Change the time of a daily notification."
        context["buttons"] = [(reverse_lazy("mood:notification_delete", args=[self.kwargs["id"]]), "Delete Notification")]
        return context

    def get_success_url(self):
        return reverse_lazy("mood:notification_list")

    def get_object(self):
        return get_object_or_404(NotificationDailySchedule, notification__recipient=self.request.user, id=self.kwargs["id"])


class NotificationDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "mood/notification_delete.html"
    model = NotificationDailySchedule

    def get_object(self):
        return get_object_or_404(NotificationDailySchedule, notification__recipient=self.request.user, id=self.kwargs["id"])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.notification.delete()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse_lazy("mood:notification_list")

class MoodStatisticsView(LoginRequiredMixin, TemplateView):
    template_name = "mood/statistics.html"

    def get_context_data(self, **kwargs):
        startdate = self.request.GET.get("start")
        enddate = self.request.GET.get("end")

        if enddate:
            maxdate = datetime.strptime(enddate, "%Y-%m-%d")
        else:
            maxdate = timezone.now()

        if startdate:
            mindate = datetime.strptime(startdate, "%Y-%m-%d")
        else:
            mindate = maxdate - relativedelta.relativedelta(weeks=1)

        context = super().get_context_data(**kwargs)
        context["title"] = "Statistics"
        context["activities"] = activitystats(self.request.user)
        return context

class MoodCSVView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        res = HttpResponse(content_type="text/csv")
        res["content-disposition"] = 'filename="mood.csv"'

        startdate = request.GET.get("start")
        enddate = request.GET.get("end")

        maxdate = None
        mindate = None

        if enddate:
            maxdate = datetime.strptime(enddate, "%Y-%m-%d")

            if not startdate:
                mindate = maxdate - relativedelta.relativedelta(weeks=1)

        if startdate:
            mindate = datetime.strptime(startdate, "%Y-%m-%d")

            if not enddate:
                maxdate = mindate + relativedelta.relativedelta(weeks=1)

        if not maxdate:
            maxdate = timezone.now()
            mindate = maxdate - relativedelta.relativedelta(weeks=1)

        output = "date,value"

        for status in Status.objects.filter(user=request.user, timestamp__gte=mindate, timestamp__lte=maxdate):
            if status.mood:
                date = status.timestamp.strftime("%Y-%m-%d %H:%M")
                output += f"\n{date},{status.mood.value}"

        res.write(output)
        return res

class MoodPlotView(LoginRequiredMixin, View):
    @method_decorator(xframe_options_sameorigin)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        res = HttpResponse(content_type="text/html")

        startdate = request.GET.get("start")
        enddate = request.GET.get("end")

        if enddate:
            maxdate = datetime.strptime(enddate, "%Y-%m-%d")
        else:
            maxdate = timezone.now()

        if startdate:
            mindate = datetime.strptime(startdate, "%Y-%m-%d")
        else:
            mindate = maxdate - relativedelta.relativedelta(weeks=1)

        res.write(hvhtml(moodstats(request.user)))
        return res