from django.dispatch import Signal

send_message = Signal()
message_sent = Signal()
message_received = Signal()