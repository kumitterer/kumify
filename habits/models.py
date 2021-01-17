from django.db import models
from django.utils import timezone

from colorfield.fields import ColorField
from polymorphic.models import PolymorphicModel
from dateutil.relativedelta import relativedelta

from common.fields import WeekdayField, DayOfMonthField

# Create your models here.

class Habit(models.Model):
    name = models.CharField(max_length=64)
    icon = models.CharField(default="fas fa-user-clock", max_length=64)
    color = ColorField(default="#000000")
    description = models.TextField(null=True, blank=True)

class HabitSchedule(PolymorphicModel):
    habit = models.ForeignKey(Habit, models.CASCADE)
    active = models.BooleanField(default=True)

    @property
    def next_scheduled(self, today=True, now=timezone.now()):
        raise NotImplementedError("%s does not implement next_scheduled." % self.__class__)

class MonthlyHabitSchedule(HabitSchedule):
    day = DayOfMonthField()

    @property
    def next_scheduled(self, today=True, now=timezone.now()):
        if self.day < now.day:
            date = now + relativedelta(months=1) + relativedelta(day=self.day)
        elif self.day == now.day:
            date = now if today else now + relativedelta(months=1)
        else:
            date = now + relativedelta(day=self.day)

            if date.date() == now.date() and not today:
                date = now + relativedelta(months=1) + relativedelta(day=self.day)

        return date.date()

class WeeklyHabitSchedule(HabitSchedule):
    weekdays = WeekdayField()

    @property
    def next_scheduled(self, today=True, now=timezone.now()):
        found = None
        for weekday in self.weekdays:
            on = now + relativedelta(weekday=weekday)
            if on < now:
                on += relativedelta(weeks=1)
            if on.day == now.day:
                if today:
                    found = now
                    break
                on += relativedelta(weeks=1)
            if (not found) or on.date() < found.date():
                found = on

        return found.date()

class DailyHabitSchedule(HabitSchedule):
    @property
    def next_scheduled(self, today=True, now=timezone.now()):
        if self.active:
            return (now if today else (now + relativedelta(days=1))).date()

class DateHabitSchedule(HabitSchedule):
    date = models.DateField()

    @property
    def next_scheduled(self, today=True, now=timezone.now()):
        if self.active and ((self.date > now.date()) or (today and (self.date == now.date()))):
            return self.date