from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=111)
    password = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=7, default='None', choices=[('male', 'Male'), ('female', 'Female')])
    bio = models.TextField(default=f"Hello! My name is {{name}}", max_length=400, blank=True, null=True)
    social_links = models.URLField(max_length=222, null=True, blank=True)
    image = models.ImageField(upload_to='profile-image/',
                              default='https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg')
    followers = models.ManyToManyField('self', 'my_followers', symmetrical=False)
    following = models.ManyToManyField('self', 'my_following', symmetrical=False)
    date = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    @property
    def following_count(self):
        return self.following.count()

    @property
    def followers_count(self):
        return self.followers.count()
