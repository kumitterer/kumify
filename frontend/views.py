from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, login
from django.urls import reverse_lazy

from .templatetags.dashboard import dashboard_styles, dashboard_scripts


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "frontend/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Dashboard"
        context["subtitle"] = (
            "An overview of everything going on in your Kumify account."
        )
        context["scripts"] = dashboard_scripts()
        context["styles"] = dashboard_styles()
        return context


class UserRegistrationView(CreateView):
    form_class = UserCreationForm
    model = get_user_model()
    template_name = "registration/registration_form.html"

    def form_valid(self, form):
        ret = super().form_valid(form)
        login(self.request, self.object)
        return ret

    def get_success_url(self):
        return reverse_lazy("frontend:dashboard")
