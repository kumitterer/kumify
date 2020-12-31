from django.db import models
from django.contrib.auth import get_user_model

from common.fields import PercentageField

class EmotionRecord(models.Model):
    emotion = models.CharField(max_length=128)
    percentage = PercentageField()
    description = models.TextField()

class ThoughtRecord(models.Model):
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    title = models.CharField(blank=True, null=True, max_length=128)
    situation = models.TextField(blank=True, null=True)
    emotions = models.ManyToManyField(EmotionRecord)
    thoughts = models.TextField(blank=True, null=True)
    pro_facts = models.TextField(blank=True, null=True)
    con_facts = models.TextField(blank=True, null=True)
    realistic = models.TextField(blank=True, null=True)
    outcome = models.TextField(blank=True, null=True)
    emotions_now = models.ManyToManyField(EmotionRecord, related_name="emotions_now")
    complete = models.BooleanField(default=False)