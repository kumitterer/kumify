from django.shortcuts import render

from django.views.generic import TemplateView, ListView, UpdateView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from .models import Dream, DreamTheme, DreamMedia, Theme
from .forms import DreamForm

from common.helpers import get_upload_path
from msgio.models import NotificationDailySchedule, Notification

class DreamListView(LoginRequiredMixin, ListView):
    template_name = "dreams/dream_list.html"
    model = Dream

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Dream List"
        context["subtitle"] = "A list of the dreams you have entered so far."
        context["buttons"] = [(reverse_lazy("dreams:dream_create"), "New Dream", "plus")]
        return context

    def get_queryset(self):
        return Dream.objects.filter(user=self.request.user).order_by('timestamp')


class DreamViewView(LoginRequiredMixin, DetailView):
    template_name = "dreams/dream_view.html"
    model = Dream

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "View Dream"
        context["subtitle"] = "View the details of your dream."
        context["buttons"] = [(reverse_lazy("dreams:dream_edit", kwargs={"id": self.kwargs["id"]}), "Edit Dream", "pen")]
        return context

    def get_object(self):
        return get_object_or_404(Dream, user=self.request.user, id=self.kwargs["id"])


class DreamCreateView(LoginRequiredMixin, CreateView):
    template_name = "dreams/dream_edit.html"
    form_class = DreamForm
    model = Dream

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Dream"
        context["subtitle"] = "What did you dream?"
        context["scripts"] = ["frontend/js/dropdown-to-buttons.js"]
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        ret = super().form_valid(form)

        for theme in form.cleaned_data["themes"]:
            if theme.user == self.request.user:
                DreamTheme.objects.create(theme=theme, dream=form.instance)

        for attachment in form.cleaned_data["uploads"]:
            dba = DreamMedia(dream=form.instance)
            dba.media.save(get_upload_path(form.instance, dba.media.name), attachment)
            dba.save()

        return ret

    def get_success_url(self):
        return reverse_lazy("dreams:dream_view", kwargs={"id": self.object.id})


class DreamEditView(LoginRequiredMixin, UpdateView):
    template_name = "dreams/dream_edit.html"
    form_class = DreamForm
    model = Dream

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Dream"
        context["subtitle"] = "Change details of a dream you entered before."
        context["scripts"] = ["frontend/js/dropdown-to-buttons.js"]
        context["buttons"] = [(reverse_lazy("dreams:dream_delete", kwargs={"id": self.kwargs["id"]}), "Delete Dream", "trash-alt")]
        return context

    def get_object(self):
        return get_object_or_404(Dream, user=self.request.user, id=self.kwargs["id"])

    def form_valid(self, form):
        for theme in form.cleaned_data["themes"]:
            if theme.user == self.request.user:
                if not theme in form.instance.theme_set:
                    DreamTheme.objects.create(theme=theme, dream=form.instance)

        for dreamtheme in form.instance.dreamtheme_set.all():
            if not dreamtheme.theme in form.cleaned_data["themes"]:
                dreamtheme.delete()

        for attachment in form.cleaned_data["uploads"]:
            dba = DreamMedia(dream=form.instance)
            dba.media.save(get_upload_path(form.instance, attachment.name), attachment)
            dba.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("dreams:dream_view", kwargs={"id": self.object.id})


class DreamDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "dreams/dream_delete.html"
    model = Dream

    def get_object(self):
        return get_object_or_404(Dream, user=self.request.user, id=self.kwargs["id"])

    def get_success_url(self):
        return reverse_lazy("dreams:dream_list")


class ThemeListView(LoginRequiredMixin, ListView):
    template_name = "dreams/theme_list.html"
    model = Theme

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Themes"
        context["subtitle"] = "The themes you have defined for your dreams."
        context["buttons"] = [(reverse_lazy("dreams:theme_create"), "Create Theme", "pen")]
        return context

    def get_queryset(self):
        return Theme.objects.filter(user=self.request.user)


class ThemeEditView(LoginRequiredMixin, UpdateView):
    template_name = "dreams/theme_edit.html"
    model = Theme
    fields = ["name", "icon", "color"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Theme"
        context["subtitle"] = "Make changes to the theme."
        context["scripts"] = ["colorfield/jscolor/jscolor.js", "colorfield/colorfield.js", "frontend/js/fontawesome-iconpicker.min.js", "frontend/js/iconpicker-loader.js"]
        context["styles"] = ["frontend/css/fontawesome-iconpicker.min.css"]
        context["buttons"] = [(reverse_lazy("dreams:theme_delete", kwargs={"id": self.kwargs["id"]}), "Delete Theme", "trash-alt")]
        return context

    def get_object(self):
        return get_object_or_404(Theme, user=self.request.user, id=self.kwargs["id"])

    def get_success_url(self):
        return reverse_lazy("dreams:theme_list")


class ThemeCreateView(LoginRequiredMixin, CreateView):
    template_name = "dreams/theme_edit.html"
    model = Theme
    fields = ["name", "icon", "color"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Theme"
        context["subtitle"] = "Add a new theme for your dreams."
        context["scripts"] = ["colorfield/jscolor/jscolor.js", "colorfield/colorfield.js", "frontend/js/fontawesome-iconpicker.min.js", "frontend/js/iconpicker-loader.js"]
        context["styles"] = ["frontend/css/fontawesome-iconpicker.min.css"]
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("dreams:theme_list")


class ThemeDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "dreams/theme_delete.html"
    model = Theme

    def get_object(self):
        return get_object_or_404(Theme, user=self.request.user, id=self.kwargs["id"])

    def get_success_url(self):
        return reverse_lazy("dreams:theme_list")


class NotificationListView(LoginRequiredMixin, ListView):
    template_name = "dreams/notification_list.html"
    model = NotificationDailySchedule
    fields = ["time"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Notifications"
        context["subtitle"] = "The daily reminders you have set up."
        context["buttons"] = [(reverse_lazy("dreams:notification_create"), "New Notification", "plus")]
        return context

    def get_queryset(self):
        return NotificationDailySchedule.objects.filter(notification__recipient=self.request.user, notification__app="dreams")


class NotificationCreateView(LoginRequiredMixin, CreateView):
    template_name = "dreams/notification_edit.html"
    model = NotificationDailySchedule
    fields = ["time"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Notification"
        context["subtitle"] = "Add a new daily notification."
        return context

    def form_valid(self, form):
        notification = Notification.objects.create(content="What did you dream tonight? Go to %KUMIFYURL% to document your dreams!", recipient=self.request.user, app="dreams")
        obj = form.save(commit=False)
        obj.notification = notification
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("dreams:notification_list")


class NotificationEditView(LoginRequiredMixin, UpdateView):
    template_name = "dreams/notification_edit.html"
    model = NotificationDailySchedule
    fields = ["time"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Notification"
        context["subtitle"] = "Change the time of a daily notification."
        context["buttons"] = [(reverse_lazy("dreams:notification_delete", args=[self.kwargs["id"]]), "Delete Notification")]
        return context

    def get_success_url(self):
        return reverse_lazy("dreams:notification_list")

    def get_object(self):
        return get_object_or_404(NotificationDailySchedule, notification__recipient=self.request.user, id=self.kwargs["id"])


class NotificationDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "dreams/notification_delete.html"
    model = NotificationDailySchedule

    def get_object(self):
        return get_object_or_404(NotificationDailySchedule, notification__recipient=self.request.user, id=self.kwargs["id"])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.notification.delete()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse_lazy("dreams:notification_list")