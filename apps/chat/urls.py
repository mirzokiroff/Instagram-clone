from django.urls import path
from chat.views import MessageViewSet

urlpatterns = [
    path('', MessageViewSet.as_view(), name='chat'),
]
