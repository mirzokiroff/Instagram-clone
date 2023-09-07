from django.db import models
from conf import settings


class Media(models.Model):
    POST = 'post'
    STORY = 'story'
    TYPE_CHOICES = [
        (POST, 'Post'),
        (STORY, 'Story'),
    ]

    post = models.CharField(max_length=10, choices=TYPE_CHOICES)
    story = models.TextField(blank=True)
    uploaded_file = models.FileField(upload_to='media/', blank=True, null=True)

    def __str__(self):
        return f"{self.post}: {self.story}"


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    archived = models.ManyToManyField(settings.ARCHIVED_POSTS, blank=True)
    tag = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tags")
    date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=222)
    media = models.ManyToManyField(Media, related_name='posts')
    text = models.TextField()

    # Accessibility info
    alt_text = models.TextField()
    image_description = models.TextField(blank=True)
    location_description = models.TextField(blank=True)
    audio_description = models.TextField(blank=True)

    def __str__(self):
        return self.text


class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Story(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    media = models.ManyToManyField(Media, related_name='stories')
    description = models.TextField(blank=True, max_length=111)
    mention = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="mentioned_users")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class StoryLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_stories', blank=True)
    shared_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_stories', blank=True)


class Highlight(models.Model):
    name = models.CharField(max_length=111)
    date = models.DateTimeField(auto_now_add=True)
    story = models.ManyToManyField(Story)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class CommentLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
