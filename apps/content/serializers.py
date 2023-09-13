from collections import OrderedDict

from rest_framework.exceptions import ValidationError
from rest_framework.fields import SkipField, HiddenField, CurrentUserDefault, ListField
from rest_framework.relations import PKOnlyObject
from rest_framework.serializers import ModelSerializer
from apps.content.models import *


class MediaSerializer(ModelSerializer):  # noqa
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Media
        fields = '__all__'


class PostSerializer(ModelSerializer):
    # id = CharField(read_only=True)
    media = ListField(validators=(file_ext_validator,))
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


class PostLikeSerializer(ModelSerializer):  # noqa
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = PostLike
        fields = '__all__'


class StoryLikeSerializer(ModelSerializer):  # noqa
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = StoryLike
        fields = '__all__'


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
