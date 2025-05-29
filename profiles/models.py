from django.db import models
from django.contrib.auth import get_user_model

from annoying.fields import AutoOneToOneField


class UserProfile(models.Model):
    user = AutoOneToOneField(get_user_model(), on_delete=models.CASCADE)
    pgp_key = models.TextField(blank=True)

    display_name = models.CharField(max_length=128, blank=True, null=True)
    timezone = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.display_name or self.user.username
