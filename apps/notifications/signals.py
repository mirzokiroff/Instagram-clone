# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.utils.html import strip_tags
# from django.template.loader import render_to_string
# from django.core.mail import send_mail
# from .models import Notification, ReelsLike, Comment, CommentLike, StoryLike, PostLike
# from users.models import UserProfile
#
#
# @receiver(post_save, sender=ReelsLike)
# def reel_like_notification(sender, instance, **kwargs):
#     # Sizga kerakli xabar va foydalanuvchi obyektini olish
#     user = instance.reel.owner
#     sender_user = instance.user
#     message = f"{sender_user.username} sizning reel'ingizga like bosdi"
#
#     # Notification obyektini yaratish
#     Notification.objects.create(
#         user=user,
#         sender=sender_user,
#         message=message,
#         reel_like_notification=instance,
#     )
#
#
# # Boshqa signal funksiyonlarini ham qo'shing (Comment, CommentLike, StoryLike, PostLike)
#
# @receiver(post_save, sender=PostLike)
# def post_like_notification(sender, instance, **kwargs):
#     user = instance.post.owner
#     sender_user = instance.user
#     message = f"{sender_user.username} sizning post'ingizga like bosdi"
#
#     Notification.objects.create(
#         user=user,
#         sender=sender_user,
#         message=message,
#         reel_like_notification=instance
#     )
