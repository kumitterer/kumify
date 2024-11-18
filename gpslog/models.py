from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

from uuid import uuid4


class GPSTrack(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    user = models.ForeignKey(get_user_model(), models.CASCADE)


class GPSToken(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    track = models.ForeignKey(GPSTrack, models.CASCADE)
    token = models.UUIDField(default=uuid4)

    # Permissions
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
    history = models.BooleanField(default=False)


class GPSPoint(models.Model):
    track = models.ForeignKey(GPSTrack, models.CASCADE)
    point = models.PointField()
    timestamp = models.DateTimeField()
    token = models.ForeignKey(GPSToken, models.SET_NULL, null=True)

    # Optional additional information
    battery = models.FloatField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True)
    speed = models.FloatField(null=True, blank=True)
    bearing = models.FloatField(null=True, blank=True)
    satellites = models.IntegerField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
