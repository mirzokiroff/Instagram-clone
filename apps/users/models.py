from django.db.models import Model, CharField, TextField, URLField, ManyToManyField, ImageField, \
    BooleanField
from django.contrib.auth.models import AbstractUser


# Create your models here.


# class CustomUserManager(UserManager):
#     use_in_migrations = True
#
#     def _create_user(self, email, password, **extra_fields):
#
#         if not email:
#             raise ValueError("The given username must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.password = make_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, email=None, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", False)
#         extra_fields.setdefault("is_superuser", False)
#         return self._create_user(email, password, **extra_fields)
#
#     def create_superuser(self, email=None, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#
#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")
#
#         return self._create_user(email, password, **extra_fields)


# class User(AbstractUser):
#     email = EmailField(max_length=222, unique=True)
#     username = None
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []
#     objects = CustomUserManager()


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

    # email = EmailField(max_length=222, unique=True)
    # username = None
    #
    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []
    # objects = CustomUserManager()

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def followers_count(self):
        return self.followers.count()
