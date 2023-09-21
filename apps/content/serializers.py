from collections import OrderedDict

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SkipField, HiddenField, CurrentUserDefault, ListField, CharField
from rest_framework.relations import PKOnlyObject, PrimaryKeyRelatedField
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from apps.content.models import Media, Post, PostLike, StoryLike, Story, Reels, CommentLike, Highlight, Comment, \
    ReelsLike
from apps.users.models import UserProfile


class MediaSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Media
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at',)


class PostSerializer(ModelSerializer):
    id = CharField(read_only=True)
    media = ListField()
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Post
        exclude = ['username']
        read_only_fields = ('created_at', 'updated_at', 'likes', 'comments', 'id')

    def create(self, validated_data):
        medias = validated_data.pop('media', [])
        media_ids = []
        if len(medias) > 10:
            raise ValidationError('media files must be less than 10')
        for media in medias:
            file = Media.objects.create(file=media, user=validated_data['user'])
            media_ids.append(file.id)
        validated_data['media'] = media_ids
        return super().create(validated_data)

    def to_representation(self, instance):
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            elif hasattr(attribute, 'all'):
                ret[field.field_name] = [field.file for field in attribute.all()]
            else:
                ret[field.field_name] = field.to_representation(attribute)
        return ret


class ReelsSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Reels
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at',)


class StorySerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Story
        fields = '__all__'
        read_only_fields = ('id', 'viewers', 'created_at', 'updated_at',)


class CommentSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at',)

    def create(self, validated_data):
        user: UserProfile = validated_data['user']
        post_id: Post = validated_data['post']
        reel_id: Reels = validated_data['reels']

        if post_id and reel_id:
            return {'error': 'You must specify either "post" or "reels".'}

        if post_id:
            post_comment = Comment.objects.create(user=user, post=post_id)
            post_id.post_comments.add(post_comment)
            post_id.save()
            return {'message ': 'You have successfully commented'}
        if reel_id:
            reel_comment = Comment.objects.create(user=user, reels=reel_id)
            reel_id.reels_comments.add(reel_comment)
            reel_id.save()
            return {'message ': 'You have successfully commented'}

    def to_representation(self, instance):
        if isinstance(instance, dict):
            return instance
        return super().to_representation(instance)


class HighlightSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Highlight
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at',)


class PostLikeSerializer(ModelSerializer):  # noqa
    post = PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = PostLike
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        user: UserProfile = validated_data['user']
        # user.liked_post.count()
        post = validated_data['post']
        like = post.post_likes.filter(user=user).first()
        if like:
            like.delete()
            return {'message': "You have unliked the post."}
        else:
            post_like = PostLike.objects.create(user=user, post=post)
            post.post_likes.add(post_like)
            post.save()
            return {'message': "You have liked the post."}

    def to_representation(self, instance):
        if isinstance(instance, dict):
            return instance
        return super().to_representation(instance)


class StoryLikeSerializer(ModelSerializer):  # noqa
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = StoryLike
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        user: UserProfile = validated_data['user']
        story = validated_data['story']
        like = story.story_likes.filter(user=user).first()
        if like:
            like.delete()
            return {'message ': 'You have unliked the story'}
        else:
            story_like = StoryLike.objects.create(user=user, story=story)
            story.story_likes.add(story_like)
            story.save()
            return {'message ': 'You have liked the story'}

    def to_representation(self, instance):
        if isinstance(instance, dict):
            return instance
        return super().to_representation(instance)


class ReelsLikeSerializer(ModelSerializer):  # noqa
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = ReelsLike
        exclude = ['id']
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        user: UserProfile = validated_data['user']
        reels = validated_data['reels']
        like = reels.reels_likes.filter(user=user).first()
        if like:
            like.delete()
            return {'message ': 'You have unliked the reel'}
        else:
            reel_like = ReelsLike.objects.create(user=user, reels=reels)
            reels.reels_likes.add(reel_like)
            reels.save()
            return {'message ': 'You have liked the reel'}

    def to_representation(self, instance):
        if isinstance(instance, dict):
            return instance
        return super().to_representation(instance)


class CommentLikeSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = CommentLike
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        user: UserProfile = validated_data['user']
        comment = validated_data['comment']
        like = comment.comment_likes.filter(user=user).first()
        if like:
            like.delete()
            return {'message ': 'You have unliked the comment'}
        else:
            comment_like = CommentLike.objects.create(user=user, comment=comment)
            comment.comment_likes.add(comment_like)
            comment.save()
            return {'message ': 'You have liked the comment'}

    def to_representation(self, instance):
        if isinstance(instance, dict):
            return instance
        return super().to_representation(instance)
