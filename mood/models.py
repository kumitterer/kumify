from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

import os.path

from colorfield.fields import ColorField

from common.helpers import get_upload_path

class Mood(models.Model):
    class Meta:
        ordering = ["-value"]

    user = models.ForeignKey(get_user_model(), models.CASCADE)
    name = models.CharField(max_length=64)
    icon = models.CharField(default="fas fa-star", max_length=64)
    color = ColorField(default="#000000")
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(255)])

    def __str__(self):
        return self.name

class Status(models.Model):
    class Meta:
        ordering = ["timestamp"]

    user = models.ForeignKey(get_user_model(), models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    mood = models.ForeignKey(Mood, models.SET_NULL, null=True)
    title = models.CharField(max_length=64, null=True, blank=True)
    text = models.TextField(null=True, blank=True)

    @property
    def short_text(self):
        return self.title or self.text[:64]

    @property
    def activity_set(self):
        return [sa.activity for sa in self.statusactivity_set.all()]

    def __str__(self):
        return self.short_text

class ActivityCategory(models.Model):
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    name = models.CharField(max_length=64)
    icon = models.CharField(default="fas fa-check", max_length=64)
    color = ColorField(default="#000000")

    def __str__(self):
        return self.name

class Activity(models.Model):
    class Meta:
        ordering = ["name"]

    user = models.ForeignKey(get_user_model(), models.CASCADE)
    name = models.CharField(max_length=64)
    icon = models.CharField(default="fas fa-check", max_length=64)
    color = ColorField(default="#000000")
    category = models.ForeignKey(ActivityCategory, models.SET_NULL, null=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class StatusMedia(models.Model):
    status = models.ForeignKey(Status, models.CASCADE)
    file = models.FileField(get_upload_path)

    @property
    def basename(self):
        return os.path.basename(self.file.name)

class StatusActivity(models.Model):
    status = models.ForeignKey(Status, models.CASCADE)
    activity = models.ForeignKey(Activity, models.CASCADE)
    comment = models.TextField(null=True, blank=True)

class Aspect(models.Model):
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    name = models.CharField(max_length=64)
    icon = models.CharField(null=True, blank=True, max_length=64)

class AspectRating(models.Model):
    aspect = models.ForeignKey(Aspect, models.CASCADE)
    name = models.CharField(max_length=64)
    icon = models.CharField(default="fas fa-star", max_length=64)
    color = ColorField(default="#000000")
    value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)])

class StatusAspectRating(models.Model):
    status = models.ForeignKey(Status, models.CASCADE)
    aspect_rating = models.ForeignKey(AspectRating, models.SET_NULL, null=True)
    comment = models.TextField(null=True, blank=True)
