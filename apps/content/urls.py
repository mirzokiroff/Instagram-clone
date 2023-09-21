from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.content.views import MediaViewSet, PostViewSet, ReelsViewSet, PostLikeViewSet, StoryLikeViewSet, \
    CommentLikeViewSet, ReelsLikeViewSet, StoryViewSet, CommentViewSet, HighlightViewSet

router = DefaultRouter()
router.register('media', MediaViewSet, basename='medias'),
router.register('post', PostViewSet, basename='posts'),
router.register('reel', ReelsViewSet, basename='reels'),
router.register('post-like', PostLikeViewSet, basename='post_likes'),
router.register('story', StoryViewSet, basename='story'),
router.register('highlight', HighlightViewSet, basename='highlight'),
router.register('comment', CommentViewSet, basename='comment'),

urlpatterns = [
    path('', include(router.urls)),
    path('story-like/', StoryLikeViewSet.as_view(), name='story_like'),
    path('reels-like/', ReelsLikeViewSet.as_view(), name='reels_like'),
    path('comment-like/', CommentLikeViewSet.as_view(), name='comment_like'),
    # path('save/', SaveViewSet.as_view(), name='save')
]
