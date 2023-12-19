# from celery import shared_task
# from django.utils import timezone
# from .models import Story
#
#
# @shared_task
# def auto_delete_stories():
#     # 24 soatdan avvalgi qoldirilgan story o'chirish
#     threshold_time = timezone.now() - timezone.timedelta(hours=24)
#     stories_to_delete = Story.objects.filter(date__lt=threshold_time)
#
#     for story in stories_to_delete:
#         story.delete()
