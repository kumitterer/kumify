from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from datetime import time, date

from dateutil.relativedelta import relativedelta

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
    default_refill = models.PositiveSmallIntegerField(default=1)

    prn = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)

class ScheduleChoices(models.IntegerChoices):
    DAYS = 0
    WEEKS = 1
    MONTHS = 2

class MedicationSchedule(models.Model):
    medication = models.ForeignKey(Medication, models.CASCADE)

    cycle_type = models.IntegerField(choices=ScheduleChoices.choices)
    cycle_count = models.IntegerField(default=1)

    first = models.DateField(default=date.today)
    last = models.DateField(null=True, blank=True)

    morning = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    noon = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    evening = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    night = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)

    def next(self, today=True):
        if timezone.now().date() > self.last:
            return False

        cur = self.first

        while True:
            if (timezone.now().date() < cur) or (today and timezone.now().date() == cur):
                return cur
        
            cur += relativedelta(
                days=self.cycle_count if self.cycle_type == ScheduleChoices.DAYS else 0, 
                weeks=self.cycle_count if self.cycle_type == ScheduleChoices.WEEKS else 0,
                months=self.cycle_count if self.cycle_type == ScheduleChoices.MONTHS else 0
                )

            if cur > self.last:
                return False

class MedicationCalendar(models.Model):
    class TimeChoices(models.IntegerChoices):
        MORNING = 0
        NOON = 1
        EVENING = 2
        NIGHT = 3

    date = models.DateField(default=date.today)
    time = models.IntegerField(choices=TimeChoices.choices)

    medication = models.ForeignKey(Medication, models.CASCADE)
    schedule = models.ForeignKey(MedicationSchedule, models.SET_NULL, null=True)

    count = models.DecimalField(max_digits=5, decimal_places=2)
    taken = models.BooleanField(default=False)

class HealthParameter(models.Model):
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    name = models.CharField(max_length=128)
    icon = models.CharField(max_length=64, default="fas fa-heart")
    unit = models.CharField(max_length=12, null=True, blank=True)

class HealthRecord(models.Model):
    parameter = models.ForeignKey(HealthParameter, models.CASCADE)
    value = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)