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
    active = models.BooleanField(default=True)

class HabitSchedule(PolymorphicModel):
    habit = models.ForeignKey(Habit, models.CASCADE)

    @property
    def next_scheduled(self, today=True, now=timezone.now()):
        raise NotImplementedError("%s does not implement next_scheduled." % self.__class__)

class MonthlyHabitSchedule(HabitSchedule):
    day = DayOfMonthField()

    @property
    def next_scheduled(self, today=True, now=timezone.now()):
        if self.day < now.day:
            date = now.replace(day=self.day) + relativedelta(months=1)
        elif self.day == now.day:
            date = now if today else now + relativedelta(months=1)
        else:
            date = now + relativedelta(day=self.day)

        return date.date()

class WeeklyHabitSchedule(HabitSchedule):
    weekdays = WeekdayField()

class DailyHabitSchedule(HabitSchedule):
    pass
