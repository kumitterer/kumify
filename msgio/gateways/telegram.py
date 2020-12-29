from django.conf import settings
from django.views.generic import View
from django.dispatch import receiver

import json

import telegram

from ..signals import send_message
from ..models import GatewayUser

class TelegramWebhookView(View):
    def post(self, *args, **kwargs):
        pass # TODO: Implement webhook receiver and management tool

class TelegramDispatcher:
    def __init__(self, token=settings.TELEGRAM_TOKEN):
        self.bot = telegram.Bot(token=token)

    def send(self, message, chat_id):
        self.bot.sendMessage(chat_id=chat_id, text=message) 

@receiver(send_message)
def telegram_sender(sender, **kwargs):
    if kwargs["dispatcher"] == "telegram":
        notification = kwargs["notification"]

        settings = GatewayUser.objects.get(user=notification.recipient, gateway="telegram")
        chat_id = settings.gatewayusersetting_set.get(key="chat_id").value

        TelegramDispatcher().send(notification.content, chat_id)