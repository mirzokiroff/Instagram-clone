from django.urls import path, include

from .views import UserDetailView, AccountViewSet, RegisterView, LoginView, FollowersView, FollowersListAPIVIew, \
    FollowListCreateAPIVIew, ProfileRetrieveUpdateDestroyAPIView, SignInWithOauth2APIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', UserDetailView, basename='user'),

urlpatterns = [
    path('', include(router.urls)),

    path('profileee/', AccountViewSet.as_view, name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('login-with-google/', SignInWithOauth2APIView.as_view(), name='google_login'),

    path('following/', FollowListCreateAPIVIew.as_view(), name='follow_create'),
    path('followers/', FollowersListAPIVIew.as_view(), name='followers_api'),
    # who the current user is subscribed to and who has subscribed to him/her, separately-separately

    # path('followinggg/<str:username>', FollowingListAPIViewByUsername.as_view(), name='follow-api-username'),
    # path('followersggg/<str:username>', FollowersListAPIViewByUsername.as_view(), name='followers-api-username'),

    path('followers-following/<str:username>/', FollowersView.as_view(), name='followers_following'),

    path('<str:username>/', ProfileRetrieveUpdateDestroyAPIView.as_view(), name='profile_retrieve_update_destroy_api'),
]
