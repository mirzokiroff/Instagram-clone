from django.db import models
from django.db.models import CASCADE

# Create your models here.
from conf import settings


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name="message_user")
    text = models.TextField()
    to_whom = models.ForeignKey('users.UserProfile', CASCADE, related_name="message_to_whom")
    from_whom = models.ForeignKey('users.UserProfile', CASCADE, related_name="message_from_whom")
    date = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField('users.UserProfile', related_name='message_like')
    # media = models.ForeignKey(settings.MEDIA, on_delete=models.SET_NULL, null=True, blank=True)
