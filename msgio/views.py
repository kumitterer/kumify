from django.http import HttpResponse
from django.views import View


class TelegramWebhookView(View):
    def post(self, request, *args, **kwargs):
        # TODO: Implement the logic to handle the incoming message
        return HttpResponse(status=200)
