from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class PercentageField(models.FloatField):
    default_validators = [MaxValueValidator(100), MinValueValidator(0)]