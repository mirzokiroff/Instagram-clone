from django.db.models import ForeignKey, CASCADE, CharField, BooleanField

from conf import settings
from shared.models import BaseModel


class Notification(BaseModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='notification_user')
    content_type = CharField(max_length=255)
    owner = CharField(max_length=111)
    object_id = CharField(max_length=111)
    action = CharField(max_length=255)
    is_read = BooleanField(default=False)
    description = CharField(max_length=222)
