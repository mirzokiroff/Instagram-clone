from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.content.views import *

router = DefaultRouter()
router.register('media', MediaViewSet, basename='media'),
router.register('post', PostViewSet, basename='post'),
router.register('post-like', PostLikeViewSet, basename='post_like'),
router.register('story-like', StoryLikeViewSet, basename='story_like'),
router.register('comment-like', CommentLikeViewSet, basename='comment_like'),

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router.urls)),
    path('story/<int:pk>/', StoryViewSet.as_view(), name='story'),
    path('highlight/<int:pk>/', HighlightViewSet.as_view(), name='highlight'),
    path('comment/<int:pk>/', CommentViewSet.as_view(), name='comment'),
    path('', include(router.urls)),
    path('', include(router.urls)),
    path('', include(router.urls)),
]
