from django.core.exceptions import ValidationError
from django.db.models import Model, ForeignKey, ManyToManyField, DateTimeField, CharField, TextField, \
    URLField
from django.db.models import CASCADE
# from django.core.validators import FileExtensionValidator
from conf import settings
from shared.models import BaseModel, unique_id, CustomFileExtensionValidator


# file_ext_validator = CustomFileExtensionValidator(('mp4', 'mkv', 'avi', 'webm', '3gp', 'jpg', 'jpeg', 'png', 'webp'))


class Media(Model):
    user = ForeignKey('users.UserProfile', on_delete=CASCADE)
    # file = FileField(upload_to='posts/', validators=(file_ext_validator,))
    file = URLField(blank=True, default='https://www.instagram.com')


class Post(BaseModel):
    id = CharField(primary_key=True, unique=True, max_length=36)
    username = ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_username')
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    archived = ManyToManyField(settings.ARCHIVED_POSTS, blank=True)
    tag = ManyToManyField(settings.AUTH_USER_MODEL, related_name="tags", blank=True)
    date = DateTimeField(auto_now_add=True)
    location = CharField(max_length=222, blank=True)
    media = ManyToManyField(Media, related_name='posts')
    text = TextField(default='bu erda siz o\'ylagan ibora bor', blank=True)

    # Accessibility info
    alt_text = TextField(blank=True)
    image_description = TextField(blank=True)
    location_description = TextField(blank=True)
    audio_description = TextField(blank=True)

    def __str__(self):
        return self.text

    @property
    def get_number_of_likes(self):
        return self.likes.count()

    @property
    def get_number_of_comments(self):
        return self.comments.count()


class Reels(BaseModel):
    id = CharField(primary_key=True, default=unique_id, max_length=36)
    caption = TextField(null=True, blank=True)
    # username = ForeignKey('users.UserProfile', on_delete=CASCADE)
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    reels = ManyToManyField(Media, related_name='reels')
    location = CharField(max_length=222, null=True, blank=True)

    @property
    def get_number_of_likes(self):
        return self.likes.count()

    @property
    def get_number_of_comments(self):
        return self.comments.count()


class Comment(Model):
    parent = ForeignKey('self', CASCADE, null=True, related_name='reply_comments')
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    post = ForeignKey(Post, on_delete=CASCADE, related_name='comments', null=True)
    reels = ForeignKey(Reels, on_delete=CASCADE, related_name='comments', null=True)
    comment = TextField(max_length=400)
    posted = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        unique_together = ('post', 'reels')

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not (self.post and self.reels):
            raise ValidationError('You must specify one of the following fields to save comments, fields: "post, reel"')
        super().save(force_insert, force_update, using, update_fields)


class Story(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    story_media = ManyToManyField(Media, related_name='stories')
    mention = ManyToManyField(settings.AUTH_USER_MODEL, related_name="mentioned_users", blank=True)
    date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.story_media

    def get_number_of_likes(self):
        return self.story_media.count()


class Highlight(Model):
    user = ManyToManyField(Post, related_name='highlight_user')
    date = DateTimeField(auto_now_add=True)
    highlight = ForeignKey(Story, on_delete=CASCADE)

    def __str__(self):
        return self.user


class Likes(Model):
    username = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='username_likes')
    post_like = ForeignKey(Post, on_delete=CASCADE, related_name='post_likes', null=True, blank=True)
    reels_like = ForeignKey(Reels, on_delete=CASCADE, related_name='reel_likes', null=True, blank=True)
    story_like = ForeignKey(Story, on_delete=CASCADE, related_name='story_likes', null=True, blank=True)
    comment_like = ForeignKey(Comment, on_delete=CASCADE, related_name='comment_likes', null=True, blank=True)

    def __str__(self):
        return self.username


class PostLike(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='liked_post')
    post = ForeignKey(Post, on_delete=CASCADE, unique=True, related_name='likes')


class StoryLike(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='liked_story')
    story = ForeignKey(Story, on_delete=CASCADE, related_name='like_story')
    story_like = ForeignKey(Likes, on_delete=CASCADE, related_name='story_likes')
    shared_to = ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_stories', blank=True)


class CommentLike(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='liked_comments')
    comment = ForeignKey(Comment, on_delete=CASCADE)


class ReelsLike(Model):
    reels = ForeignKey('content.Reels', on_delete=CASCADE, related_name='likes')
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='liked_reels')
