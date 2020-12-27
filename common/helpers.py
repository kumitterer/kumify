import uuid

def get_upload_path(instance, filename):
    return 'usermedia/{0}/{1}/{2}'.format(instance.user.id, str(uuid.uuid4()), filename)