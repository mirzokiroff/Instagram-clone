from django.urls import path, include
from django.views.generic import TemplateView

from apps.users.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', UserDetailView, basename='user'),
router.register('profile', AccountViewSet, basename='profile'),

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('following', FollowListCreateAPIVIew.as_view(), name='follow-create'),
    path('following/<str:username>', FollowingListAPIViewByUsername.as_view(), name='follow-api-username'),
    path('unfollow/<str:username>', UnFollowAPIView.as_view(), name='unfollow-api'),
    path('followers', FollowersListAPIVIew.as_view(), name='followers-api'),
    path('followers-following/<str:username>', FollowersView.as_view(), name='followers-following'),
    path('followers/<str:username>', FollowersListAPIViewByUsername.as_view(), name='followers-api-username'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('<str:username>', ProfileRetrieveUpdateDestroyAPIView.as_view(), name='profile-retrieve-update-destroy-api'),
]
