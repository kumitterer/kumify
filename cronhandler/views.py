from django.views.generic import View
from django.http import HttpResponse

from .signals import cron

class CronHandlerView(View):
    def get(self, *args, **kwargs):
        cron.send_robust(self.__class__)
        return HttpResponse()