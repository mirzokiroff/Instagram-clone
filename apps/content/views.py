from rest_framework.generics import ListCreateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView

# Create your views here.
from apps.content.serializers import *


class MediaViewSet(ListCreateAPIView, DestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    lookup_field = 'pk'


class PostViewSet(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'


class PostLikeViewSet(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    lookup_field = 'pk'


class StoryViewSet(ListCreateAPIView, DestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    lookup_field = 'pk'


class StoryLikeViewSet(ListCreateAPIView, DestroyAPIView):
    queryset = StoryLike.objects.all()
    serializer_class = StoryLikeSerializer
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
