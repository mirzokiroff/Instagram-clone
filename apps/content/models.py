from django.db.models import Model, ForeignKey, ManyToManyField, DateTimeField, CharField, TextField, \
    URLField
from django.db.models import CASCADE
from conf import settings
from shared.models import BaseModel, unique_id


# file_ext_validator = CustomFileExtensionValidator(('mp4', 'mkv', 'avi', 'webm', '3gp', 'jpg', 'jpeg', 'png', 'webp'))


class Media(BaseModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='media_user')
    # file = FileField(upload_to='posts/', validators=(file_ext_validator,))
    file = URLField(blank=True, default='https://www.instagram.com')
    date = DateTimeField(auto_now_add=True)


class Post(BaseModel):
    id = CharField(primary_key=True, unique=True, max_length=36, default=unique_id)
    username = ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_username')
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    # archived = ManyToManyField(settings.ARCHIVED_POSTS, blank=True)
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
        return self.post_likes.count()

    @property
    def get_number_of_comments(self):
        return self.post_comments.count()


class Reels(BaseModel):
    id = CharField(primary_key=True, unique=True, max_length=36, default=unique_id)
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='reels_user')
    caption = TextField(null=True, blank=True)
    reels = ManyToManyField(Media, related_name='reels')

    @property
    def get_number_of_likes(self):
        return self.reels_likes.count()

    @property
    def get_number_of_comments(self):
        return self.reels_comments.count()


class Comment(BaseModel):
    id = CharField(primary_key=True, unique=True, max_length=36, default=unique_id)
    parent = ForeignKey('self', CASCADE, null=True, related_name='reply_comments')
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='comment_user')
    comments = TextField(max_length=333)
    date = DateTimeField(auto_now_add=True)
    post = ForeignKey('content.Post', on_delete=CASCADE, related_name='post_comments', null=True, blank=True)
    reels = ForeignKey('content.Reels', on_delete=CASCADE, related_name='reels_comments', null=True, blank=True)

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
    id = CharField(primary_key=True, unique=True, max_length=36, default=unique_id)
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='story_user')
    story = ManyToManyField(Media, related_name='stories')
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
    id = CharField(primary_key=True, unique=True, max_length=36, default=unique_id)
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='highlight_user')
    name = CharField(max_length=77)
    date = DateTimeField(auto_now_add=True)
    highlight = ForeignKey(Story, on_delete=CASCADE, related_name='highlight')

    def __str__(self):
        return self.user


class Viewers(BaseModel):
    post = ForeignKey(Post, CASCADE, related_name='post_view')
    reel = ForeignKey(Reels, CASCADE, related_name='reel_view')
    story = ForeignKey(Story, CASCADE, related_name='story_view')


class PostLike(BaseModel):
    user = ForeignKey('users.UserProfile', CASCADE, related_name='post_like_user')
    post = ForeignKey('content.Post', CASCADE, related_name='post_likes')

    def __str__(self):
        return 'Like: ' + self.user.username


class StoryLike(BaseModel):
    user = ForeignKey('users.UserProfile', CASCADE, related_name='story_like_user')
    story = ForeignKey('content.Story', CASCADE, related_name='story_likes')
    shared_to = ForeignKey('users.UserProfile', CASCADE, related_name='shared_stories', null=True, blank=True)

    def __str__(self):
        return 'Like: ' + self.user.username


class CommentLike(BaseModel):
    user = ForeignKey('users.UserProfile', CASCADE, related_name='comment_liked_user')
    comment = ForeignKey('content.Comment', CASCADE, related_name='comment_likes')

    def __str__(self):
        return 'Like: ' + self.user.username


class ReelsLike(BaseModel):
    user = ForeignKey('users.UserProfile', CASCADE, related_name='reels_like_user')
    reels = ForeignKey('content.Reels', CASCADE, related_name='reels_likes')

    def __str__(self):
        return 'Like: ' + self.user.username
