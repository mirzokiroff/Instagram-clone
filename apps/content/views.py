from django.utils.decorators import method_decorator
from drf_yasg import utils, openapi
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from content.serializers import PostSerializer, StorySerializer, StoryLikeSerializer, \
    CommentSerializer, HighlightSerializer, ReelsSerializer, PostLikeSerializer, ReelsLikeSerializer, \
    CommentLikeSerializer, UpdatePostSerializer
from content.models import ReelsLike, Post, Reels, Story, StoryLike, PostLike, Highlight, Comment, CommentLike


@method_decorator(name='create', decorator=utils.swagger_auto_schema(manual_parameters=[openapi.Parameter(
    name='media',
    in_=openapi.IN_FORM,
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_FILE),
    required=True,
    description='media'
)]))
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [AllowAny]
    http_method_names = ('get', 'post', 'patch', 'delete')

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()

        if request.user == post.user or request.user.is_staff:
            post.delete()
            return Response({"message": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "You can't delete the post"}, status=status.HTTP_403_FORBIDDEN)

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return UpdatePostSerializer
        return super().get_serializer_class()


class ReelsViewSet(ModelViewSet):
    queryset = Reels.objects.all()
    serializer_class = ReelsSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    http_method_names = ('get', 'post', 'patch', 'delete')

    def destroy(self, request, *args, **kwargs):
        reels = self.get_object()

        if request.user == reels.user or request.user.is_staff:
            reels.delete()
            return Response({"message": "You delete the reels"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "You can't delete the reels"}, status=status.HTTP_403_FORBIDDEN)


class StoryViewSet(ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    http_method_names = ('get', 'post', 'delete')

    def destroy(self, request, *args, **kwargs):
        story = self.get_object()

        if story.user == request.user or request.user.is_staff:
            story.delete()
            return Response({"message": "You delete the story"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "You can't delete the story"}, status=status.HTTP_403_FORBIDDEN)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ('get', 'post', 'delete')

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()

        if comment.user == request.user or request.user.is_staff:
            comment.delete()
            return Response({"message": "You delete the story"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "You can't delete the story"}, status=status.HTTP_403_FORBIDDEN)


class HighlightViewSet(ModelViewSet):
    queryset = Highlight.objects.all()
    serializer_class = HighlightSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ('get', 'post', 'patch', 'delete')

    def destroy(self, request, *args, **kwargs):
        highlight = self.get_object()

        if highlight.user == request.user or request.user.is_staff:
            highlight.delete()
            return Response({"message": "You delete the story"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "You can't delete the story"}, status=status.HTTP_403_FORBIDDEN)


class PostLikeViewSet(ListCreateAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]


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
