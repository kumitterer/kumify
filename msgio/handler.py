from django.dispatch import receiver
from django.utils.timezone import localtime, now

from cronhandler.signals import cron

from .models import Notification

@receiver(cron)
def send_notifications(sender, **kwargs):
    returns = []
    for notification in Notification.objects.all():
        for datetime in notification.notificationdatetimeschedule_set.all():
            if not datetime.sent and datetime.datetime <= localtime(now()):
                try:
                    returns.append(notification.send())
                    datetime.sent = True
                    datetime.save()
                except Exception:
                    pass # TODO: Implement some sort of error logging / admin notification
        for daily in notification.notificationdailyschedule_set.all():
            if ((not daily.last_sent) or daily.last_sent < localtime(now()).date()) and daily.time <= localtime(now()).time():
                try:
                    returns.append(notification.send())
                    daily.last_sent = localtime(now()).date()
                    daily.save()
                except Exception:
                    pass # TODO: See above

    return returns

