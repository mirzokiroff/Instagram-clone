from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from apps.users.models import UserProfile
from rest_framework.fields import IntegerField, DateTimeField, HiddenField, CurrentUserDefault
from rest_framework.relations import SlugRelatedField


# from apps.content.serializers import *


class UserProfileSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    date = DateTimeField(read_only=True)

    class Meta:
        model = UserProfile
        exclude = ['is_superuser', 'first_name', 'last_name', 'is_staff', 'groups', 'user_permissions', 'last_login',
                   'date_joined', 'followers', 'following']

        def to_representation(self, instance):
            data = super().to_representation(instance)
            data['followers'] = instance.followers_count
            data['following'] = instance.following_count
            return data



class UserViewProfileModelSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'fullname', 'username', 'image')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context['request']
        data['is_followed'] = False
        if request and (user := getattr(request, 'user')) and user.is_authenticated:
            data['is_followed'] = user.following.filter(id=instance.id).exists()
        return data


class UserFollowModelSerializer(ModelSerializer):
    followers = UserViewProfileModelSerializer(many=True)
    following = UserViewProfileModelSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('following', 'followers')

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
        # if user.following.filter(id=follow_user.id).first():
        #     user.following.remove(follow_user)
        #     follow_user.followers.remove(user)
        #     follow_user.save()
        #     user.save()
        # else:
        user.following.add(follow_user)
        user.save()
        follow_user.followers.add(user)
        follow_user.save()
        return user

    def to_representation(self, instance):
        return {'message': "you've followed successfully"}


class UserSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'password', 'user']


class LoginSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'password']
        username = serializers.CharField(max_length=111)
        password = serializers.CharField(write_only=True)


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['is_superuser', 'first_name', 'last_name', 'is_staff', 'groups', 'user_permissions', 'last_login',
                   'date_joined', 'followers', 'following']
