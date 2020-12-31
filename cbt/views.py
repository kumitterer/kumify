from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ThoughtRecordStepOneForm
from .models import ThoughtRecord

class ThoughtRecordStepOneView(LoginRequiredMixin, CreateView):
    form_class = ThoughtRecordStepOneForm
    template_name = "cbt/thoughtrecord1.html"
    model = ThoughtRecord

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Thought Record"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        ret = super().form_valid(form)

        return ret