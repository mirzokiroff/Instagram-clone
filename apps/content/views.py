from rest_framework.generics import *

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from apps.content.serializers import *


class MediaViewSet(ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    lookup_field = 'pk'


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'


class PostLikeViewSet(ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    lookup_field = 'pk'
    http_method_names = ('get', 'post', 'get_id', 'delete')


class StoryViewSet(ListCreateAPIView, DestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    lookup_field = 'pk'


class StoryLikeViewSet(ModelViewSet):
    queryset = StoryLike.objects.all()
    serializer_class = StoryLikeSerializer
    http_method_names = ('get', 'get_id', 'post', 'delete')
    lookup_field = 'pk'


class CommentViewSet(ListCreateAPIView, DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'


class CommentLikeViewSet(ListCreateAPIView, DestroyAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    lookup_field = 'pk'


class HighlightViewSet(ListCreateAPIView, DestroyAPIView):
    queryset = Highlight.objects.all()
    serializer_class = HighlightSerializer
    lookup_field = 'pk'
