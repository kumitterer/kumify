from django.views.generic import TemplateView, ListView, UpdateView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .models import Status, Activity, Mood, StatusMedia, StatusActivity
from .forms import StatusForm


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
            StatusMedia.objects.create(status=form.instance, file=attachment)

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
            StatusMedia.objects.create(status=form.instance, file=attachment)
        
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