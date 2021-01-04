from django.db import models
from django.contrib.auth import get_user_model

from datetime import time

class MedicationSettings(models.Model):
    user = models.ForeignKey(get_user_model(), models.CASCADE)

    morning_from = models.TimeField(default=time(6))
    morning_till = models.TimeField(default=time(10))

    noon_from = models.TimeField(default=time(12))
    noon_till = models.TimeField(default=time(14))

    evening_from = models.TimeField(default=time(19))
    evening_till = models.TimeField(default=time(21))

    night_from = models.TimeField(default=time(22))
    night_till = models.TimeField(default=time(23))

    notifications = models.BooleanField(default=True)
    refill_reminder = models.PositiveSmallIntegerField(default=7)

class Medication(models.Model):
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    name = models.CharField(max_length=128)
    icon = models.CharField(max_length=64, default="fas fa-tablets")

    supply = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    default_refill = models.PositiveSmallIntegerField(null=True, blank=True)

    morning = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    noon = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    evening = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    night = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)

    remarks = models.TextField(null=True, blank=True)