from django import forms

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["display_name", "timezone", "pgp_key"]
        widgets = {
            "pgp_key": forms.Textarea(attrs={"rows": 6, "cols": 40}),
            "timezone": forms.TextInput(attrs={"placeholder": "e.g., Europe/Vienna"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["display_name"].required = False
        self.fields["timezone"].required = False
        self.fields["pgp_key"].required = False
