from django.db.models import ForeignKey, CASCADE, CharField, IntegerField, BooleanField

from conf import settings
from shared.models import BaseModel


class Notification(BaseModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='notifications')
    content_type = CharField(max_length=255)
    object_id = IntegerField()
    action = CharField(max_length=255)  # 'like', 'unlike', etc.
    is_read = BooleanField(default=False)
