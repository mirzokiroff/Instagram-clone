from django.core.validators import FileExtensionValidator
from django.db.models import Model, ForeignKey, ManyToManyField, DateTimeField, CharField, TextField, FileField
from django.db.models import CASCADE

from conf import settings
from shared.models import BaseModel, unique_id, CustomFileExtensionValidator

file_ext_validator = CustomFileExtensionValidator(('mp4', 'mkv', 'avi', 'webm', '3gp', 'jpg', 'jpeg', 'png', 'webp'))


class Media(Model):
    # user = ForeignKey('users.UserProfile', CASCADE, related_name='media_user', blank=True)
    file = FileField(upload_to='posts/', validators=(file_ext_validator,))
    date = DateTimeField(auto_now_add=True)


class Share(BaseModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='share_user')
    post_shared_to = ForeignKey('users.UserProfile', CASCADE, related_name='shared_post', null=True, blank=True)
    reels_shared_to = ForeignKey('users.UserProfile', CASCADE, related_name='shared_reels', null=True, blank=True)
    story_shared_to = ForeignKey('users.UserProfile', CASCADE, related_name='shared_story', null=True, blank=True)
    highlight_shared_to = ForeignKey('users.UserProfile', CASCADE, related_name='shared_highlight', null=True,
                                     blank=True)


class Post(BaseModel):
    id = CharField(primary_key=True, max_length=36, default=unique_id)
    # username = ManyToManyField('users.UserProfile', CASCADE, related_name='post_username')
    user = ForeignKey('users.UserProfile', CASCADE, related_name='post_user')
    tag = ForeignKey('users.UserProfile', CASCADE, related_name="post_tags", blank=True, null=True)
    date = DateTimeField(auto_now_add=True)
    location = CharField(max_length=222, blank=True, null=True)
    media = ManyToManyField('content.Media', related_name='posts',
                            validators=[FileExtensionValidator(
                                ['mp4', 'mkv', 'avi', 'webm', '3gp', 'jpg', 'jpeg', 'png', 'webp'])])
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


class Reels(BaseModel):
    id = CharField(primary_key=True, max_length=36, default=unique_id)
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='reels_user')
    caption = TextField(null=True, blank=True)
    media = FileField(upload_to='reels/', validators=[FileExtensionValidator(['mp4', 'avi', 'mkv'])])

    @property
    def get_number_of_likes(self):
        return self.reels_likes.count()

    @property
    def get_number_of_comments(self):
        return self.reels_comments.count()


class Comment(BaseModel):
    id = CharField(primary_key=True, max_length=36, default=unique_id)
    # parent = ForeignKey('self', CASCADE, null=True, related_name='reply_comments')
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='comment_user')
    comments = TextField(max_length=333)
    date = DateTimeField(auto_now_add=True)
    post = ForeignKey('content.Post', CASCADE, related_name='post_comments', null=True, blank=True)
    reels = ForeignKey('content.Reels', CASCADE, related_name='reels_comments', null=True, blank=True)

    def __str__(self):
        return self.comments

    @property
    def get_number_of_likes(self):
        return self.comment_likes

    @property
    def get_number_of_reply_comment(self):
        return self.parent

    class Meta:
        unique_together = ('post', 'reels')


class Story(BaseModel):
    id = CharField(primary_key=True, max_length=36, default=unique_id)
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='story_user')
    story = FileField(upload_to='story/', validators=[FileExtensionValidator(['mp4', 'jpg', 'png'])])
    mention = ForeignKey('users.UserProfile', CASCADE, related_name="mentioned_users", null=True, blank=True)
    # viewer = ForeignKey('users.UserProfile', CASCADE, related_name='story_viewers')
    date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.story

    @property
    def get_number_of_viewers(self):
        return self.story_view.count()

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
        return self.user


class Viewers(BaseModel):
    post = ForeignKey('content.Post', CASCADE, related_name='post_view')
    reel = ForeignKey('content.Reels', CASCADE, related_name='reel_view')
    story = ForeignKey('content.Story', CASCADE, related_name='story_view')


class PostLike(BaseModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='post_like_user')
    post = ForeignKey('content.Post', CASCADE, related_name='post_likes')
    share_to = ForeignKey('content.Share', CASCADE, related_name='post_share')

    def __str__(self):
        return 'Like: ' + self.user.username


class StoryLike(BaseModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='story_like_user')
    story = ForeignKey('content.Story', CASCADE, related_name='story_likes')
    share_to = ForeignKey('content.Share', CASCADE, related_name='story_share')

    def __str__(self):
        return 'Like: ' + self.user.username


class CommentLike(BaseModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='comment_liked_user')
    comment = ForeignKey('content.Comment', CASCADE, related_name='comment_likes')

    def __str__(self):
        return 'Like: ' + self.user.username


class ReelsLike(BaseModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='reels_like_user')
    reels = ForeignKey('content.Reels', CASCADE, related_name='reels_likes')
    share_to = ForeignKey('content.Share', CASCADE, related_name='reels_share')

    def __str__(self):
        return 'Like: ' + self.user.username


class HighlightLike(BaseModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='highlight_like_user')
    highlight = ForeignKey('content.Highlight', CASCADE, related_name='highlight_like')
    share_to = ForeignKey('content.Share', CASCADE, related_name='highlight_share')

    def __str__(self):
        return 'Like: ' + self.user.username
