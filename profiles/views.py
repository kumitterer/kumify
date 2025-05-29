from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import UserProfile
from .forms import UserProfileForm

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profiles/profile_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        context['profile'] = profile
        context['title'] = "Your Profile"
        context['subtitle'] = "View your user profile information."
        return context

class UserProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = "profiles/profile_edit.html"
    success_url = reverse_lazy('profiles:profile_view')

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Edit Profile"
        context['subtitle'] = "Update your profile information."
        return context