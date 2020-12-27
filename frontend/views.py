from django.views.generic import TemplateView, ListView, UpdateView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "frontend/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Dashboard"
        context["subtitle"] = "An overview of everything going on in your Kumify account."
        return context