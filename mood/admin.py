from django.contrib import admin

from mood.models import Status, Mood, Activity, StatusMedia, StatusActivity, Aspect, AspectRating, StatusAspectRating

class StatusAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user", "mood", "short_text")

class ActivityAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "icon")

admin.site.register(Status, StatusAdmin)
admin.site.register(Mood)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(StatusMedia)
admin.site.register(StatusActivity)
admin.site.register(Aspect)
admin.site.register(AspectRating)
admin.site.register(StatusAspectRating)