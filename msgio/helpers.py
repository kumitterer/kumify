import filtersignals

from dbsettings.functions import getValue

make_message = filtersignals.FilterSignal()

def run_filters(notification):
    return make_message.send_robust(notification.__class__, recipient=notification.recipient, content=notification.content, app=notification.app, data=notification.data, _protected=["data"])["content"]

@filtersignals.receiver(make_message, 500)
def notification_placeholders(sender, **kwargs):
    return {"content": kwargs["content"].replace("%KUMIFYURL%", getValue("KUMIFY_URL", "your Kumify instance"))}