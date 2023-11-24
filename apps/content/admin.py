from django.contrib import admin
from content.models import Post, PostLike, ReelsLike, Reels, Story, StoryLike, Share, CommentLike, Comment, \
    HighlightLike, Highlight, Notification, Viewers

# Register your models here.
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(Reels)
admin.site.register(ReelsLike)
admin.site.register(Share)
admin.site.register(Story)
admin.site.register(StoryLike)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(Highlight)
admin.site.register(HighlightLike)
admin.site.register(Notification)
admin.site.register(Viewers)
