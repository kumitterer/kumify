from django.forms import ModelForm, ModelMultipleChoiceField

from multiupload.fields import MultiFileField

from .models import Dream, Theme

class DreamForm(ModelForm):
    uploads = MultiFileField(required=False)
    themes = ModelMultipleChoiceField(queryset=Theme.objects.all())

    class Meta:
        model = Dream
        fields = ["timestamp", "mood", "title", "content", 'type', 'wet', 'lucid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mood"].required = False