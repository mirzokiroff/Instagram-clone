from django.core.validators import FileExtensionValidator
from django.db.models import Model, ForeignKey, ManyToManyField, DateTimeField, CharField, TextField, FileField, \
    BooleanField
from django.db.models import CASCADE

from conf import settings
from shared.models import BaseModel, unique_id, CustomFileExtensionValidator
from users.models import UserProfile

file_ext_validator = CustomFileExtensionValidator(
    ('mp4', 'mkv', 'avi', 'webm', '3gp', 'jpg', 'jpeg', 'png', 'webp', 'mov'))


class Media(BaseModel):
    user = ForeignKey('users.UserProfile', CASCADE, related_name='media_user', null=True, blank=True)
    file = FileField(upload_to='posts/', validators=(file_ext_validator,))
    date = DateTimeField(auto_now_add=True)


class Post(BaseModel):
    id = CharField(primary_key=True, max_length=36, default=unique_id)
    # username = ManyToManyField('users.UserProfile', CASCADE, related_name='post_username')
    user = ForeignKey('users.UserProfile', CASCADE, related_name='post_user')
    tag = ForeignKey('users.UserProfile', CASCADE, related_name="post_tags", blank=True, null=True)
    date = DateTimeField(auto_now_add=True)
    location = CharField(max_length=222, blank=True, null=True)
    media = ManyToManyField('content.Media', related_name='posts')
    text = TextField(default='bu erda siz o\'ylagan ibora bor', blank=True, null=True)

    # Accessibility info
    alt_text = TextField(blank=True, null=True)
    image_description = TextField(blank=True, null=True)
    location_description = TextField(blank=True, null=True)
    audio_description = TextField(blank=True, null=True)

    def __str__(self):
        return self.text

    @property
    def get_number_of_likes(self):
        return self.post_likes.count()

    @property
    def get_number_of_comments(self):
        return self.post_comments.count()

    def get_number_of_viewers(self):
        return self.post_view.count()


class Reels(BaseModel):
    id = CharField(primary_key=True, max_length=36, default=unique_id)
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='reels_user')
    caption = TextField(null=True, blank=True)
    media = FileField(upload_to='reels/', validators=[FileExtensionValidator(['mp4', 'avi', 'mkv', 'mov'])])

    @property
    def get_number_of_likes(self):
        return self.reels_likes.count()

    @property
    def get_number_of_comments(self):
        return self.reels_comments.count()


class Comment(BaseModel):
    id = CharField(primary_key=True, max_length=36, default=unique_id)
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='comment_user')
    comment = TextField()
    date = DateTimeField(auto_now_add=True)
    post = ForeignKey('content.Post', CASCADE, related_name='post_comments', null=True, blank=True)
    reels = ForeignKey('content.Reels', CASCADE, related_name='reels_comments', null=True, blank=True)

    def __str__(self):
        return self.comment

    @property
    def get_number_of_likes(self):
        return self.comment_likes

    class Meta:
        unique_together = ('post', 'reels')


class Story(BaseModel):
    id = CharField(primary_key=True, max_length=36, default=unique_id)
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='story_user')
    story = FileField(upload_to='story/', validators=[FileExtensionValidator(['mp4', 'jpg', 'png', 'mov'])])
    mention = ForeignKey('users.UserProfile', CASCADE, related_name="mentioned_users", null=True, blank=True)
    viewer = ForeignKey('users.UserProfile', CASCADE, related_name='story_viewers', null=True, blank=True)
    date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.story

    def get_viewers_info(self):
        viewers_info = []
        for viewer_relation in self.story_view.all():
            viewer = viewer_relation
            viewer_info = {
                'username': viewer.user,
                'full_name': viewer.get_full_name(),
                'avatar': viewer.user if viewer.userprofile.avatar else None,
            }
            viewers_info.append(viewer_info)
        return viewers_info

    @property
    def get_number_of_likes(self):
        return self.story_likes.count()


class Highlight(BaseModel):
    id = CharField(primary_key=True, max_length=36, default=unique_id)
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='highlight_user')
    name = CharField(max_length=77)
    date = DateTimeField(auto_now_add=True)
    highlight = ForeignKey('content.Story', CASCADE, related_name='highlight')

    def __str__(self):
        return self.user.username  # noqa

    @property
    def get_numbers_of_likes(self):
        return self.highlight_likes.count()


class Viewers(BaseModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='user_view')
    post = ForeignKey('content.Post', CASCADE, related_name='post_view')
    reel = ForeignKey('content.Reels', CASCADE, related_name='reel_view')
    story = ForeignKey('content.Story', CASCADE, related_name='story_view')


class PostLike(BaseModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='post_like_user', null=True, blank=True)
    post = ForeignKey('content.Post', CASCADE, related_name='post_likes')

    def __str__(self):
        return 'Like: ' + self.user.username  # noqa


class StoryLike(BaseModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='story_like_user')
    story = ForeignKey('content.Story', CASCADE, related_name='story_likes')

    def __str__(self):
        return 'Like: ' + self.user.username  # noqa


class CommentLike(BaseModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='comment_liked_user')
    comment = ForeignKey('content.Comment', CASCADE, related_name='comment_likes')

    def __str__(self):
        return 'Like: ' + self.user.username  # noqa


class ReelsLike(BaseModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='reels_like_user')
    reels = ForeignKey('content.Reels', CASCADE, related_name='reels_likes')

    def __str__(self):
        return 'Like: ' + self.user.username  # noqa


class HighlightLike(BaseModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='highlight_like_user')
    highlight = ForeignKey('content.Highlight', CASCADE, related_name='highlight_likes')

    def __str__(self):
        return 'Like: ' + self.user.username  # noqa


class Share(BaseModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='share_user')
    receiver = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='receiver_post')
    post_shared_to = ForeignKey('content.Post', CASCADE, related_name='shared_post', null=True, blank=True)
    reels_shared_to = ForeignKey('content.Reels', CASCADE, related_name='shared_reels', null=True, blank=True)
    story_shared_to = ForeignKey('content.Story', CASCADE, related_name='shared_story', null=True, blank=True)
    highlight_shared_to = ForeignKey('content.Highlight', CASCADE, related_name='shared_highlight', null=True,
                                     blank=True)


# class Notification(BaseModel):
#     user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='notification_to_user')
#     sender = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='notification_from_user')
#     message = CharField(max_length=77, blank=True)
#     is_seen = BooleanField(default=False)
#     date = DateTimeField(auto_now_add=True)
#     reel_like_notification = ForeignKey('content.ReelsLike', CASCADE, related_name='notification_reel_like', blank=True,
#                                         null=True)
#     comment_notification = ForeignKey('content.Comment', CASCADE, related_name='notification_comment', blank=True,
#                                       null=True)
#     comment_like_notification = ForeignKey('content.CommentLike', CASCADE, related_name='notification_comment_like',
#                                            blank=True, null=True)
#     story_like_notification = ForeignKey('content.StoryLike', CASCADE, related_name='notification_story_like',
#                                          blank=True, null=True)
#     post_like_notification = ForeignKey('content.PostLike', CASCADE, related_name='notification_post_like', blank=True,
#                                         null=True)
#     followers_notification = ForeignKey('users.UserProfile', CASCADE, related_name='notification_followers', blank=True,
#                                         null=True)
