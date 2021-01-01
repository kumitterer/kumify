from django.contrib import admin

from .models import Dream, DreamMedia, DreamTheme, Theme

admin.site.register(Dream)
admin.site.register(DreamMedia)
admin.site.register(DreamTheme)
admin.site.register(Theme)