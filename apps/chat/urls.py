from django.urls import path
from apps.chat.views import *

urlpatterns = [
    path('', MessageViewSet.as_view(), name='chat'),
]
