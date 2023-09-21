from rest_framework.generics import ListCreateAPIView, DestroyAPIView

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import *
from apps.content.serializers import *
from apps.content.models import ReelsLike


class MediaViewSet(ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    http_method_names = ('get', 'post', 'delete')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    http_method_names = ('get', 'post', 'patch', 'delete')


class ReelsViewSet(ModelViewSet):
    queryset = Reels.objects.all()
    serializer_class = ReelsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    http_method_names = ('get', 'post', 'patch', 'delete')


class StoryViewSet(ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    http_method_names = ('get', 'post', 'delete')


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ('get', 'post', 'delete')


class HighlightViewSet(ModelViewSet):
    queryset = Highlight.objects.all()
    serializer_class = HighlightSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    http_method_names = ('get', 'post', 'patch', 'delete')


class PostLikeViewSet(ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ('get', 'post')


class StoryLikeViewSet(ListCreateAPIView):
    queryset = StoryLike.objects.all()
    serializer_class = StoryLikeSerializer
    permission_classes = [IsAuthenticated]


class CommentLikeViewSet(ListCreateAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]


class ReelsLikeViewSet(ListCreateAPIView):
    queryset = ReelsLike.objects.all()
    serializer_class = ReelsLikeSerializer
    permission_classes = [IsAuthenticated]
