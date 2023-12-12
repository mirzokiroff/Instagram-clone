from django.urls import path, include
from rest_framework.routers import DefaultRouter

from content.views import PostViewSet, ReelsViewSet, PostLikeViewSet, StoryLikeViewSet, \
    CommentLikeViewSet, ReelsLikeViewSet, StoryViewSet, CommentViewSet, HighlightViewSet, ShareViewSet, \
    HighlightLikeViewSet

router = DefaultRouter()
router.register('post', PostViewSet, basename='posts'),
router.register('reel', ReelsViewSet, basename='reels'),
router.register('story', StoryViewSet, basename='story'),  #
router.register('highlight', HighlightViewSet, basename='highlight'),
router.register('comment', CommentViewSet, basename='comment'),

urlpatterns = [
    path('', include(router.urls)),
    path('share/', ShareViewSet.as_view(), name='share'),
    path('post-like/', PostLikeViewSet.as_view(), name='post_like'),
    path('story-like/', StoryLikeViewSet.as_view(), name='story_like'),
    path('reels-like/', ReelsLikeViewSet.as_view(), name='reels_like'),
    path('highlight-like/', HighlightLikeViewSet.as_view(), name='highlight_like'),
    path('comment-like/', CommentLikeViewSet.as_view(), name='comment_like'),
]
