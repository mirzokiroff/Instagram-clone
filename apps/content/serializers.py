from collections import OrderedDict
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SkipField, HiddenField, CurrentUserDefault, CharField
from rest_framework.relations import PKOnlyObject, PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from apps.content.models import Media, Post, PostLike, StoryLike, Story, Reels, Likes, CommentLike, Highlight, Comment
from apps.users.models import UserProfile


class MediaSerializer(ModelSerializer):  # noqa
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Media
        fields = '__all__'


class PostSerializer(ModelSerializer):
    # id = CharField(read_only=True)
    # media = ListField(validators=(file_ext_validator,))
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


class UpdatePostModelSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = 'text', 'location'
        read_only_fields = ('created_at', 'updated_at', 'likes', 'comments', 'id')

    def to_representation(self, instance):
        return PostSerializer(instance).data


class ReelsSerializer(ModelSerializer):  # noqa
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Reels
        fields = '__all__'


class StorySerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Story
        fields = '__all__'


class CommentSerializer(ModelSerializer):  # noqa
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'


class HighlightSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Highlight
        fields = '__all__'


class LikesSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Likes
        fields = '__all__'


class PostLikeSerializer(ModelSerializer):  # noqa
    post = PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = PostLike
        fields = '__all__'

    def create(self, validated_data):
        user: UserProfile = validated_data['user']
        # user.liked_post.count()
        post = validated_data['post']
        like = post.likes.filter(user=user).first()
        if like:
            like.delete()
            return {'message': "You have unliked the post."}
        else:
            post_like = PostLike.objects.create(user=user, post=post)
            post.likes.add(post_like)
            post.save()
            return {'message': "You have liked the post."}

    def to_representation(self, instance):
        return instance


class StoryLikeSerializer(ModelSerializer):  # noqa
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = StoryLike
        exclude = ['story_like', ]

    def create(self, validated_data):
        user: UserProfile = validated_data['user']
        story = validated_data['story']
        if user != story:
            if user.likes.filter(id=story.id).first():
                story.likes.remove(story)
                user.likes.remove(user)
                story.save()
                user.save()
                return {'message': "You have unliked the story."}
            else:
                story.likes.add(story)
                user.likes.add(user)
                story.save()
                user.save()
                return {'message': "You have liked the story."}
        else:
            return {'message': "You can not like the story"}

    def to_representation(self, instance):
        return instance


class ReelsLikeSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Reels
        fields = '__all__'


class CommentLikeSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = CommentLike
        fields = '__all__'
