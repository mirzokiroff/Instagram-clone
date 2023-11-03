from django.contrib.auth.hashers import make_password
from django.db.models import Model, CharField, TextField, URLField, ManyToManyField, ImageField, \
    BooleanField, EmailField
from django.contrib.auth.models import AbstractUser, UserManager
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


# Create your models here.
class BearerTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None

        token = parts[1]
        try:
            user = UserProfile.objects.all(username=token)
            return (user, None)
        except UserProfile.DoesNotExist:
            raise AuthenticationFailed('Invalid Authorization')


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):

        if not username:
            username = email.split('@')[0]

        email = self.normalize_email(email)
        username = self.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class UserProfile(AbstractUser):
    fullname = CharField(max_length=111, default='new_user', blank=True, null=True)
    password = CharField(max_length=255, null=True, blank=True)
    gender = CharField(max_length=7, default='None', choices=[('male', 'Male'), ('female', 'Female')], null=True,
                       blank=True)
    bio = TextField(max_length=255, blank=True, null=True)
    social_links = URLField(max_length=222, null=True, blank=True, default='https://www.instagram.com')
    image = ImageField(upload_to='profile-image/',
                       default='https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg')
    followers = ManyToManyField(to='self', related_name='my_followers', symmetrical=False)
    following = ManyToManyField(to='self', related_name='my_following', symmetrical=False)
    likes = ManyToManyField(to='self', related_name='my_likes', symmetrical=False)
    is_public = BooleanField(default=True)

    email = EmailField(max_length=222, unique=True)
    # name = CharField(max_length=255, unique=True)

    # USERNAME_FIELD = "name"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def avatar(self):
        default = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg'
        try:
            return self.image.url if self.image else default
        except (KeyError, AttributeError, TypeError):
            return default

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.fullname
