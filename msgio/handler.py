from django.dispatch import receiver
from django.utils.timezone import now

from cronhandler.signals import cron

from .models import Notification

@receiver(cron)
def send_notifications(sender, **kwargs):
    returns = []
    for notification in Notification.objects.all():
        for datetime in notification.notificationdatetimeschedule_set.all():
            if not datetime.sent and datetime.datetime <= now():
                try:
                    returns.append(notification.send())
                    datetime.sent = True
                    datetime.save()
                except:
                    pass # TODO: Implement some sort of error logging / admin notification
        for daily in notification.notificationdailyschedule_set.all():
            if ((not daily.last_sent) or daily.last_sent < now().date()) and daily.time <= now().time():
                try:
                    returns.append(notification.send())
                    daily.last_sent = now().date()
                    daily.save()
                except:
                    pass # TODO: See above

    return returns