from django.contrib import admin

from .models import GatewayUser, GatewayUserSetting, Notification, NotificationDailySchedule, NotificationDatetimeSchedule, NotificationDispatcher

# Register your models here.

admin.site.register(GatewayUser)
admin.site.register(GatewayUserSetting)
admin.site.register(Notification)
admin.site.register(NotificationDailySchedule)
admin.site.register(NotificationDatetimeSchedule)
admin.site.register(NotificationDispatcher)