from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer

from content.models import Post
from users.models import UserProfile, UserSearch
from rest_framework.fields import IntegerField, DateTimeField, HiddenField, CurrentUserDefault, CharField, \
    SerializerMethodField, ReadOnlyField
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField

from users.oauth2 import oauth2_sign_in


class UserProfileSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    date = DateTimeField(format='%d-%m-%Y', read_only=True)
    last_login = DateTimeField(format='%d-%m-%Y', read_only=True)
    following = IntegerField(source='following.count', read_only=True)
    followers = IntegerField(source='followers.count', read_only=True)

    user_posts = ReadOnlyField(source='user_posts.values_list', read_only=True)
    user_reels = ReadOnlyField(source='user_reels.values_list', read_only=True)
    user_stories = ReadOnlyField(source='user_stories.values_list', read_only=True)
    user_highlights = ReadOnlyField(source='user_highlights.values_list', read_only=True)

    # likes = IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = UserProfile
        exclude = ['likes', 'is_superuser', 'is_staff', 'groups', 'user_permissions', 'is_active', 'date_joined',
                   'password', 'email']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['image'] = instance.avatar

        user_posts = instance.user_posts.values_list('id', flat=True)
        data['user_posts'] = [str(post_id) for post_id in user_posts]

        user_reels = instance.user_reels.values_list('id', flat=True)
        data['user_reels'] = [str(reel_id) for reel_id in user_reels]

        user_stories = instance.user_stories.values_list('id', flat=True)
        data['user_stories'] = [str(story_id) for story_id in user_stories]

        user_highlights = instance.user_highlights.values_list('id', flat=True)
        data['user_highlights'] = [str(highlight_id) for highlight_id in user_highlights]

        return data


class UserViewProfileModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = UserProfile
        fields = ('fullname', 'username', 'image', 'user')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context['request']
        data['is_followed'] = False
        if request and (user := getattr(request, 'user')) and user.is_authenticated:  # noqa
            data['is_followed'] = user.following.filter(id=instance.id).exists()
        return data


class UserFollowModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    followers = UserViewProfileModelSerializer(many=True)
    following = UserViewProfileModelSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('following', 'followers', 'user')

    def create(self, validated_data):
        return super().create(validated_data)


class UserFollowingModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    username = SlugRelatedField(queryset=UserProfile.objects.all(), slug_field='username')

    class Meta:
        model = UserProfile
        fields = ('username', 'user')

    def create(self, validated_data):
        user: UserProfile = validated_data['user']
        follow_user = validated_data['username']
        if user != follow_user:
            if user.following.filter(id=follow_user.id).first():
                user.following.remove(follow_user)
                follow_user.followers.remove(user)
                follow_user.save()
                user.save()
                return {'message': "you have successfully unsubscribed"}
            else:
                user.following.add(follow_user)
                user.save()
                follow_user.followers.add(user)
                follow_user.save()
                return {'message': "you have successfully subscribed"}
        else:
            return {'message': "you cannot subscribe to yourself"}

    def to_representation(self, instance):
        return instance


class FollowersSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    followers = SlugRelatedField(many=True, read_only=True, slug_field='username')
    following = SlugRelatedField(many=True, read_only=True, slug_field='username')

    class Meta:
        model = UserProfile
        fields = ('username', 'followers', 'following', 'user')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        user = request.user.username
        for follow in data.get("followers", None):
            if user == follow:
                data['is_following'] = True
                break
        else:
            data['is_following'] = False
        return data


class UserSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'user']


class LoginSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'password']
        username = CharField(max_length=111)
        password = CharField(write_only=True)
        # confirm_password = CharField(write_only=True)


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'first_name', 'email', 'password')


class SignInWithOauth2Serializer(Serializer):
    token = CharField(required=True)

    def validate_token(self, token):  # noqa
        user = oauth2_sign_in(token)

        if user is None:
            raise ValidationError('Invalid token')

        return user


class SearchUserSerializer(ModelSerializer):
    class Meta:
        model = UserSearch
        fields = ['id', 'search']


class EmailVerySerializer(Serializer):
    code = CharField(max_length=5)
