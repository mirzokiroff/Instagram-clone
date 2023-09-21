from django.db.models import Model, CharField, TextField, URLField, ManyToManyField, ImageField, \
    BooleanField
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    fullname = CharField(max_length=111, default='string', blank=True)
    password = CharField(max_length=255, null=True, blank=True)
    gender = CharField(max_length=7, default='None', choices=[('male', 'Male'), ('female', 'Female')])
    bio = TextField(max_length=400, blank=True, null=True)
    social_links = URLField(max_length=222, null=True, blank=True, default='https://www.instagram.com')
    image = ImageField(upload_to='profile-image/',
                       default='https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg')
    followers = ManyToManyField('self', 'my_followers', symmetrical=False)
    following = ManyToManyField('self', 'my_following', symmetrical=False)
    likes = ManyToManyField('self', 'my_likes', symmetrical=False)
    is_public = BooleanField(default=True)

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def followers_count(self):
        return self.followers.count()
