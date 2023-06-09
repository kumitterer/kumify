from django.db import models
from django.contrib.auth import get_user_model

from .signals import send_message

# Create your models here.

class Notification(models.Model):
    content = models.TextField()
    recipient = models.ForeignKey(get_user_model(), models.CASCADE)
    app = models.CharField(max_length=64, null=True, blank=True)
    data = models.CharField(max_length=128, null=True, blank=True)

    def send(self):
        dispatchers = self.notificationdispatcher_set.all()
        response = []

        if dispatchers:
            for dispatcher in dispatchers:
                response.append(send_message.send_robust(self.__class__, dispatcher=dispatcher.dispatcher, notification=self))
        else:
            for dispatcher in GatewayUser.objects.filter(user=self.recipient):
                response.append(send_message.send_robust(self.__class__, dispatcher=dispatcher.gateway, notification=self))

        return response

class NotificationDispatcher(models.Model):
    notification = models.ForeignKey(Notification, models.CASCADE)
    dispatcher = models.CharField(max_length=64)

class NotificationDatetimeSchedule(models.Model):
    notification = models.ForeignKey(Notification, models.CASCADE)
    datetime = models.DateTimeField()
    sent = models.BooleanField(default=False)

class NotificationDailySchedule(models.Model):
    notification = models.ForeignKey(Notification, models.CASCADE)
    time = models.TimeField()
    last_sent = models.DateField(null=True, blank=True)

class GatewayUser(models.Model):
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    gateway = models.CharField(max_length=64)

class GatewayUserSetting(models.Model):
    gatewayuser = models.ForeignKey(GatewayUser, models.CASCADE)
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=256)