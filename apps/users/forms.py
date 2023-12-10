from django.contrib.auth.forms import UserCreationForm

from users.models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2')