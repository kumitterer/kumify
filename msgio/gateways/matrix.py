from django.views.generic import View
from django.dispatch import receiver

import json
import asyncio

from nio import AsyncClient

from dbsettings.functions import dbsettings

from ..signals import send_message
from ..models import GatewayUser
from ..helpers import run_filters

class MatrixDispatcher:
    def __init__(self, username=dbsettings.MATRIX_USERNAME, password=dbsettings.MATRIX_PASSWORD, homeserver=dbsettings.MATRIX_HOMESERVER):
        self.username = username
        self.password = password
        self.homeserver = homeserver

    async def send(self, message, room_id):
        client = AsyncClient(self.homeserver, self.username)
        await client.login(self.password)
        await client.join(room_id)

        await client.room_send(
            room_id=room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "body": message
            }
        )

@receiver(send_message)
def matrix_sender(sender, **kwargs):
    if kwargs["dispatcher"] == "matrix":
        notification = kwargs["notification"]

        settings = GatewayUser.objects.get(user=notification.recipient, gateway="matrix")
        room_id = settings.gatewayusersetting_set.get(key="room_id").value

        text = run_filters(notification)

        asyncio.get_event_loop().run_until_complete(MatrixDispatcher().send(text, room_id))
