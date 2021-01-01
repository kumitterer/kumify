from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth import get_user_model

from mood.models import Mood
from common.helpers import get_upload_path

from colorfield.fields import ColorField

class Theme(models.Model):
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    name = models.CharField(max_length=64)
    icon = models.CharField(default="fas fa-bed", max_length=64)
    color = ColorField(default="#000000")

    def __str__(self):
        return self.name

class Dream(models.Model):
    class DreamTypes(models.IntegerChoices):
        NIGHT = 0, 'Night (main) sleep'
        DAY = 1, 'Daydream'
        NAP = 2, 'Napping'

    user = models.ForeignKey(get_user_model(), models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=64)
    content = models.TextField()
    type = models.IntegerField(choices=DreamTypes.choices)
    mood = models.ForeignKey(Mood, models.SET_NULL, null=True)
    lucid = models.BooleanField(default=False)
    wet = models.BooleanField(default=False)

    @property
    def short_text(self):
        return self.title or self.content[:64]

    @property
    def theme_set(self):
        return [theme.theme for theme in self.dreamtheme_set.all()]

class DreamTheme(models.Model):
    dream = models.ForeignKey(Dream, models.CASCADE)
    theme = models.ForeignKey(Theme, models.CASCADE)

class DreamMedia(models.Model):
    dream = models.ForeignKey(Dream, models.CASCADE)
    media = models.FileField(get_upload_path)

class ThemeRating(models.Model):
    theme = models.ForeignKey(Theme, models.CASCADE)
    name = models.CharField(max_length=64)
    icon = models.CharField(default="fas fa-star", max_length=64)
    color = ColorField(default="#000000")
    value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)])

class DreamThemeRating(models.Model):
    dream = models.ForeignKey(Dream, models.CASCADE)
    theme_rating = models.ForeignKey(ThemeRating, models.SET_NULL, null=True)
    comment = models.TextField(null=True, blank=True)
