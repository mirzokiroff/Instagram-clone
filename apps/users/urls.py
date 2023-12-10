from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterView, LoginView, FollowersListAPIVIew, \
    FollowListCreateAPIVIew, ProfileUpdateAPIView, SignInWithOauth2APIView, SearchHistoryView, \
    SearchUserView, SearchHistoryDeleteDestroyView, FollowersFollowingView, FollowersFollowingDetailView

router = DefaultRouter()
# router.register('user', UserDetailView, basename='user'),

urlpatterns = [
    path('', include(router.urls)),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('login-with-google/', SignInWithOauth2APIView.as_view(), name='google_login'),

    path('following/', FollowListCreateAPIVIew.as_view(), name='follow_create'),
    path('followers/', FollowersListAPIVIew.as_view(), name='followers_api'),

    path('followers-following/<str:username>/', FollowersFollowingView.as_view(), name='followers_following'),

    path('followers-following- detail/', FollowersFollowingDetailView.as_view(), name='followers_following_detail'),

    path('profile', ProfileUpdateAPIView.as_view(), name='profile_retrieve_update_destroy_api'),

    path("search-history/", SearchHistoryView.as_view(), name="searches"),
    path("search/<str:username>/", SearchUserView.as_view(), name="user_search"),
    path("search-history/<int:pk>/", SearchHistoryDeleteDestroyView.as_view(), name="search-delete"),

]
