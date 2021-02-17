from django.apps import AppConfig

import msgio.gateways.matrix
import msgio.gateways.telegram

class MsgioConfig(AppConfig):
    name = 'msgio'
