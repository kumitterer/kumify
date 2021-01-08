from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, validate_comma_separated_integer_list

from multiselectfield import MultiSelectField

class WeekdayChoices(models.IntegerChoices):
    MONDAY = 0, "Monday"
    TUESDAY = 1, "Tuesday"
    WEDNESDAY = 2, "Wednesday"
    THURSDAY = 3, "Thursday"
    FRIDAY = 4, "Friday"
    SATURDAY = 5, "Saturday"
    SUNDAY = 6, "Sunday"

class PercentageField(models.FloatField):
    default_validators = [MaxValueValidator(100), MinValueValidator(0)]

class WeekdayField(MultiSelectField):
    def __init__(self, *args, **kwargs):
        self.choices = WeekdayChoices.choices
        super().__init__(*args, **kwargs)

class DayOfMonthField(models.PositiveIntegerField):
    default_validators = [MinValueValidator(1), MaxValueValidator(31)]