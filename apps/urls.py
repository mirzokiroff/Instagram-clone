from django.urls import path, include

urlpatterns = [
    path('user/', include('users.urls')),
    path('post/', include('content.urls')),
    path('chat - chat is temporarily down/', include('chat.urls')),
    path('notifications/', include('notifications.urls')),
]
