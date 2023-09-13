from rest_framework.generics import *

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import *
from apps.content.serializers import *


class MediaViewSet(ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class ReelsViewSet(ModelViewSet):
    queryset = Reels.objects.all()
    serializer_class = ReelsSerializer
    lookup_field = 'pk'


class StoryViewSet(ListCreateAPIView, DestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    lookup_field = 'pk'


class CommentViewSet(ListCreateAPIView, DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'


class HighlightViewSet(ListCreateAPIView, DestroyAPIView):
    queryset = Highlight.objects.all()
    serializer_class = HighlightSerializer
    lookup_field = 'pk'


class PostLikeViewSet(ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    lookup_field = 'pk'
    http_method_names = ('get', 'post', 'get_id', 'delete')


class StoryLikeViewSet(ModelViewSet):
    queryset = StoryLike.objects.all()
    serializer_class = StoryLikeSerializer
    http_method_names = ('get', 'get_id', 'post', 'delete')
    lookup_field = 'pk'


class CommentLikeViewSet(ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    lookup_field = 'pk'
    http_method_names = ('get', 'get_id', 'post', 'delete')


class ReelsLikeViewSet(ModelViewSet):
    queryset = ReelsLike
    serializer_class = ReelsLikeSerializer
    lookup_field = 'pk'
    http_method_names = ('get', 'get_id', 'post', 'delete')
