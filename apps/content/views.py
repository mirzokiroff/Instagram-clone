from django.utils.decorators import method_decorator
from drf_yasg import utils, openapi
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from content.serializers import PostSerializer, StorySerializer, StoryLikeSerializer, \
    CommentSerializer, HighlightSerializer, ReelsSerializer, PostLikeSerializer, ReelsLikeSerializer, \
    CommentLikeSerializer, HighlightLikeSerializer, ShareSerializer, NotificationSerializer
from content.models import ReelsLike, Post, Reels, Story, StoryLike, PostLike, Highlight, Comment, CommentLike, \
    HighlightLike, Share, Notification


class IsAuthenticatedAndOwner(BasePermission):
    message = 'You must be the owner of this object.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


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
    permission_classes = [AllowAny, IsAuthenticatedAndOwner]
    http_method_names = ('get', 'post', 'delete')

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)

        # Add the post ID to user_posts if the post's user ID matches the current user's ID
        if self.request.user.id == post.user.id:
            self.request.user.user_posts.add(post.id)

    @action(detail=True, methods=['delete'])
    def delete_post(self, request, pk=None):
        post = self.get_object()

        # Remove the post ID from user_posts if the post's user ID matches the current user's ID
        if request.user.id == post.user.id:
            request.user.user_posts.remove(post.id)

        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ReelsViewSet(ModelViewSet):
    queryset = Reels.objects.all()
    serializer_class = ReelsSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsAuthenticatedAndOwner]
    http_method_names = ('get', 'post', 'patch', 'delete')

    def perform_create(self, serializer):
        reel = serializer.save(user=self.request.user)

        # Add the post ID to user_posts if the post's user ID matches the current user's ID
        if self.request.user.id == reel.user.id:
            self.request.user.user_reels.add(reel.id)

    @action(detail=True, methods=['delete'])
    def delete_post(self, request, pk=None):
        reel = self.get_object()

        # Remove the post ID from user_posts if the post's user ID matches the current user's ID
        if request.user.id == reel.user.id:
            request.user.user_reels.remove(reel.id)

        reel.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class StoryViewSet(ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsAuthenticatedAndOwner]
    http_method_names = ('get', 'post', 'delete')

    def perform_create(self, serializer):
        story = serializer.save(user=self.request.user)

        # Add the post ID to user_posts if the post's user ID matches the current user's ID
        if self.request.user.id == story.user.id:
            self.request.user.user_stories.add(story.id)

    @action(detail=True, methods=['delete'])
    def delete_post(self, request, pk=None):
        story = self.get_object()

        # Remove the post ID from user_posts if the post's user ID matches the current user's ID
        if request.user.id == story.user.id:
            request.user.user_stories.remove(story.id)

        story.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedAndOwner]
    http_method_names = ('get', 'post', 'delete')

    def get_queryset(self):
        user_id = self.request.user
        queryset = Comment.objects.all()
        if user_id:
            queryset = queryset.filter(user=user_id)
        return queryset


class HighlightViewSet(ModelViewSet):
    queryset = Highlight.objects.all()
    serializer_class = HighlightSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedAndOwner]
    http_method_names = ('get', 'post', 'delete')

    def post(self, request):
        user_id = request.user.id
        data = request.data
        story_id = data.get('story_id', None)

        if story_id is not None:
            story = Story.objects.filter(id=story_id).first()
            if story and story.user_id == user_id:
                highlight = Highlight.objects.create(user_id=user_id, story_id=story_id)
                return Response({'message': 'Highlight created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'You are not the owner of this story'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'Story not found'}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        highlight = serializer.save(user=self.request.user)

        # Add the post ID to user_posts if the post's user ID matches the current user's ID
        if self.request.user.id == highlight.user.id:
            self.request.user.user_highlights.add(highlight.id)

    @action(detail=True, methods=['delete'])
    def delete_post(self, request, pk=None):
        highlight = self.get_object()

        # Remove the post ID from user_posts if the post's user ID matches the current user's ID
        if request.user.id == highlight.user.id:
            request.user.user_highlights.remove(highlight.id)

        highlight.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeViewSet(ListCreateAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedAndOwner]


class StoryLikeViewSet(ListCreateAPIView):
    queryset = StoryLike.objects.all()
    serializer_class = StoryLikeSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedAndOwner]


class CommentLikeViewSet(ListCreateAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedAndOwner]


class ReelsLikeViewSet(ListCreateAPIView):
    queryset = ReelsLike.objects.all()
    serializer_class = ReelsLikeSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedAndOwner]


class HighlightLikeViewSet(ListCreateAPIView):
    queryset = HighlightLike.objects.all()
    serializer_class = HighlightLikeSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedAndOwner]


class ShareViewSet(ListCreateAPIView, DestroyAPIView):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedAndOwner]
    http_method_names = 'get', 'post', 'delete'


class NotificationViewSet(ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedAndOwner]
