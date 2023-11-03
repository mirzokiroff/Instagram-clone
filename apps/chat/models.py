from django.db import models
from django.db.models import CASCADE

# Create your models here.
from conf import settings
from shared.models import BaseModel, unique_id


class Message(BaseModel):
    id = models.CharField(primary_key=True, default=unique_id, max_length=36)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name="message_user")
    message = models.TextField()
    receiver = models.ForeignKey('users.UserProfile', CASCADE, related_name="receiver")
    sender = models.ForeignKey('users.UserProfile', CASCADE, related_name="sender")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('date',)
