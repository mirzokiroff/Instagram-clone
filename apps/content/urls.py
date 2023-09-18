from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.content.views import MediaViewSet, PostViewSet, ReelsViewSet, PostLikeViewSet, StoryLikeViewSet, \
    CommentLikeViewSet, ReelsLikeViewSet, StoryViewSet, CommentViewSet, HighlightViewSet

router = DefaultRouter()
router.register('media', MediaViewSet, basename='medias'),
router.register('post', PostViewSet, basename='posts'),
router.register('reel', ReelsViewSet, basename='reels'),
router.register('post-like', PostLikeViewSet, basename='post_likes'),
router.register('story-like', StoryLikeViewSet, basename='story_likes'),
router.register('comment-like', CommentLikeViewSet, basename='comment_likes'),
router.register('reels-like', ReelsLikeViewSet, basename='reels_likes'),

urlpatterns = [
    path('', include(router.urls)),
    path('story/', StoryViewSet.as_view(), name='stories'),
    path('comment/', CommentViewSet.as_view(), name='comment'),
    path('highlight/', HighlightViewSet.as_view(), name='highlight'),
]
