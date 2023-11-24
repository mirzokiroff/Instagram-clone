from collections import OrderedDict

from rest_framework.exceptions import ValidationError
from rest_framework.fields import SkipField, HiddenField, CurrentUserDefault, ListField, CharField, FileField
from rest_framework.relations import PKOnlyObject, PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from content.models import Media, Post, PostLike, StoryLike, Story, Reels, CommentLike, Highlight, Comment, \
    ReelsLike, file_ext_validator, HighlightLike, Share, Notification
from users.models import UserProfile


class PostSerializer(ModelSerializer):
    id = CharField(read_only=True)
    media = ListField(validators=(file_ext_validator,))
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'id')

    def create(self, validated_data):
        medias = validated_data.pop('media', [])
        media_ids = []

        if len(medias) > 10:
            raise ValidationError('media files must be less than 10')

        for media in medias:
            file = Media.objects.create(file=media)
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
                ret[field.field_name] = [field.file.url for field in attribute.all()]
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret


class UpdatePostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['location']
        read_only_fields = ('created_at', 'updated_at', 'likes', 'comments', 'id')

    def to_representation(self, instance):
        return PostSerializer(instance).data


class ReelsSerializer(ModelSerializer):
    id = CharField(read_only=True)
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Reels
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'likes', 'comments', 'id', 'user')


class StorySerializer(ModelSerializer):
    id = CharField(read_only=True)
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Story
        fields = '__all__'
        read_only_fields = ('id', 'viewers', 'created_at', 'updated_at', 'user')


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
        comment: Comment = validated_data['comments']

        if post_id and reel_id:
            return {'error': 'You must specify either "post" or "reels".'}

        if post_id:
            post_comment = Comment.objects.create(user=user, post=post_id, comments=comment)
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
        read_only_fields = ('id', 'created_at', 'updated_at')


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
        read_only_fields = ('created_at', 'updated_at', 'user')

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


class HighlightLikeSerializer(ModelSerializer):  # noqa
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = HighlightLike
        exclude = ['id']
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        user: UserProfile = validated_data['user']
        highlight = validated_data['highlight']
        like = highlight.highlight_likes.filter(user=user).first()
        if like:
            like.delete()
            return {'message ': 'You have unliked the highlight'}
        else:
            highlight_like = HighlightLike.objects.create(user=user, highlight=highlight)
            highlight.highlight_likes.add(highlight_like)
            highlight.save()
            return {'message ': 'You have liked the highlight'}

    def to_representation(self, instance):
        if isinstance(instance, dict):
            return instance
        return super().to_representation(instance)

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     request = self.context.get('request')
    #     user = request.user.username
    #     for like in data.get("likes"):
    #         if user == like:
    #             data['is_liked'] = True
    #             break
    #     else:
    #         data['is_liked'] = False
    #     return data


class ShareSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Share
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def validate(self, data):
        post_shared_to = data.get('post_shared_to')
        reels_shared_to = data.get('reels_shared_to')
        story_shared_to = data.get('story_shared_to')
        highlight_shared_to = data.get('highlight_shared_to')

        non_empty_count = sum(bool(x) for x in [post_shared_to, reels_shared_to, story_shared_to, highlight_shared_to])

        if non_empty_count != 1:
            raise ValidationError(
                "You must specify only one of post_shared_to, reels_shared_to, story_shared_to, or highlight_shared_to.")

        return data


class NotificationSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'user']

    # def create(self, validated_data):
    #     user: UserProfile = validated_data['followers']
    #     reel = validated_data['notification_reel_like']
