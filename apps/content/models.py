from django.core.exceptions import ValidationError
from django.db.models import Model, ForeignKey, FileField, ManyToManyField, DateTimeField, CharField, TextField, \
    OneToOneField
from django.db.models import CASCADE
# from django.core.validators import FileExtensionValidator
from conf import settings
from shared.models import BaseModel, unique_id, CustomFileExtensionValidator

file_ext_validator = CustomFileExtensionValidator(('mp4', 'mkv', 'avi', 'webm', '3gp', 'jpg', 'jpeg', 'png', 'webp'))


class Media(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    file = FileField(upload_to='posts/', validators=(file_ext_validator,))


class Post(BaseModel):
    id = CharField(primary_key=True, default=unique_id, max_length=36)
    username = ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_username')
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    archived = ManyToManyField(settings.ARCHIVED_POSTS, blank=True)
    tag = ManyToManyField(settings.AUTH_USER_MODEL, related_name="tags", blank=True)
    date = DateTimeField(auto_now_add=True)
    location = CharField(max_length=222, blank=True)
    media = ManyToManyField(Media, related_name='posts')
    # like_by = ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_post')
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
    story = ManyToManyField(Media, related_name='stories')
    mention = ManyToManyField(settings.AUTH_USER_MODEL, related_name="mentioned_users")
    date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.story

    def get_number_of_likes(self):
        return self.story.count()


class Highlight(Model):
    name = CharField(max_length=111)
    date = DateTimeField(auto_now_add=True)
    story = ManyToManyField(Story)

    def __str__(self):
        return self.name


class PostLike(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='liked_post')
    post_owner = ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_owner')
    post = OneToOneField(Post, on_delete=CASCADE, unique=True, related_name='likes')


class StoryLike(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='liked_story')
    # like_by = ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_stories', blank=True)
    story = ForeignKey(Story, on_delete=CASCADE)
    shared_to = ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_stories', blank=True)

    def __str__(self):
        return 'Like' + self.user.username


class CommentLike(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='liked_comments')
    comment = ForeignKey(Comment, on_delete=CASCADE)

    # like_by = ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)

    def __str__(self):
        return 'Like' + self.user.username


class ReelsLike(Model):
    reels = ForeignKey('content.Reels', on_delete=CASCADE, related_name='likes')
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='liked_reels')

    def __str__(self):
        return 'Like' + self.user.username
