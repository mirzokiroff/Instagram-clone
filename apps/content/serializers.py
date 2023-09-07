from collections import OrderedDict

from rest_framework.exceptions import ValidationError
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject
from rest_framework.serializers import ModelSerializer
from apps.content.models import *


class MediaSerializer(ModelSerializer):  # noqa
    class Meta:
        model = Media
        fields = '__all__'


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
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


class PostLikeSerializer(ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'


class StorySerializer(ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'


class StoryLikeSerializer(ModelSerializer):  # noqa
    class Meta:
        model = StoryLike
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentLikeSerializer(ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'


class HighlightSerializer(ModelSerializer):
    class Meta:
        model = Highlight
        fields = '__all__'
