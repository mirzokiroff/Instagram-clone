from django.urls import path, include
from users.views import Index

urlpatterns = [
    path('user/', include('users.urls')),
    path('post/', include('content.urls')),
    path('chat/', include('chat.urls')),
    path('home/', Index.as_view(), name='index'),
]
