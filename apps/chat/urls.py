from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chat.views import MessageViewSet

router = DefaultRouter()
router.register('chat', MessageViewSet, basename='chat')
urlpatterns = [
    path('', include(router.urls)),
]
