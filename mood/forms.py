from django.forms import ModelForm, ModelMultipleChoiceField

from multiupload.fields import MultiFileField

from .models import Status, Activity

class StatusForm(ModelForm):
    uploads = MultiFileField(required=False)
    activities = ModelMultipleChoiceField(queryset=Activity.objects.all(), required=False)

    class Meta:
        model = Status
        fields = ["timestamp", "mood", "title", "text"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mood"].required = False