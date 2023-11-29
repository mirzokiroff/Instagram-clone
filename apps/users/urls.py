from django.urls import path, include

from .views import RegisterView, LoginView, FollowersView, FollowersListAPIVIew, \
    FollowListCreateAPIVIew, ProfileRetrieveUpdateDestroyAPIView, SignInWithOauth2APIView, SearchHistoryView, \
    SearchUserView, SearchHistoryDeleteDestroyView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('user', UserDetailView, basename='user'),
# router.register('profile', AccountViewSet, basename='profile'),

urlpatterns = [
    path('', include(router.urls)),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('login-with-google/', SignInWithOauth2APIView.as_view(), name='google_login'),

    path('following/', FollowListCreateAPIVIew.as_view(), name='follow_create'),
    path('followers/', FollowersListAPIVIew.as_view(), name='followers_api'),
    # who the current user is subscribed to and who has subscribed to him/her, separately-separately

    # path('followinggg/<str:username>', FollowingListAPIViewByUsername.as_view(), name='follow-api-username'),
    # path('followersggg/<str:username>', FollowersListAPIViewByUsername.as_view(), name='followers-api-username'),

    path('followers-following/<str:username>/', FollowersView.as_view(), name='followers_following'),

    path('profile', ProfileRetrieveUpdateDestroyAPIView.as_view(), name='profile_retrieve_update_destroy_api'),

    path("search-history/", SearchHistoryView.as_view(), name="searches"),
    path("search/<str:username>/", SearchUserView.as_view(), name="user_search"),
    path("search-history/<int:pk>/", SearchHistoryDeleteDestroyView.as_view(), name="search-delete")
]
