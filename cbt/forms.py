from django.forms import ModelForm

from .models import ThoughtRecord

class ThoughtRecordStepOneForm(ModelForm):
    class Meta:
        model = ThoughtRecord
        fields = ["title", "situation"]
