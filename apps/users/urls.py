from django.urls import path, include

from users.views import UserDetailView, AccountViewSet, RegisterView, LoginView, FollowersView, \
    FollowingListAPIViewByUsername, FollowersListAPIVIew, FollowListCreateAPIVIew, FollowersListAPIViewByUsername, \
    ProfileRetrieveUpdateDestroyAPIView
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
    path('followers', FollowersListAPIVIew.as_view(), name='followers-api'),
    path('followers-following/<str:username>', FollowersView.as_view(), name='followers-following'),
    path('followers/<str:username>', FollowersListAPIViewByUsername.as_view(), name='followers-api-username'),
    path('<str:username>', ProfileRetrieveUpdateDestroyAPIView.as_view(), name='profile-retrieve-update-destroy-api'),
    # path('oauth2/', SignInWithOauth2APIView.as_view(), name='oauth2-sign-in'),
]
