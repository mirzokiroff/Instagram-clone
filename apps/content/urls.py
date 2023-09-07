from django.urls import path
from apps.content.views import *

urlpatterns = [
    path('', PostViewSet.as_view(), name='post'),
    path('media/<int:pk>/', MediaViewSet.as_view(), name='media'),
    path('story/<int:pk>/', StoryViewSet.as_view(), name='story'),
    path('highlight/<int:pk>/', HighlightViewSet.as_view(), name='highlight'),
    path('comment/<int:pk>/', CommentViewSet.as_view(), name='comment'),
    path('post-like/<int:pk>/', PostLikeViewSet.as_view(), name='post_like'),
    path('story-like/<int:pk>/', StoryLikeViewSet.as_view(), name='story-like'),
    path('comment-like/<int:pk>/', CommentLikeViewSet.as_view(), name='comment-like'),
]
