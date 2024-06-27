from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterView, LoginView, FollowersListAPIVIew, \
    FollowListCreateAPIVIew, ProfileUpdateAPIView, SignInWithOauth2APIView, SearchHistoryView, \
    SearchUserView, SearchHistoryDeleteDestroyView, FollowersFollowingView, FollowersFollowingDetailView, \
    SearchUserSaveView, EmailSignUpView, LogoutView

router = DefaultRouter()
# router.register('user', UserDetailView, basename='user'),

urlpatterns = [
    path('', include(router.urls)),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login-with-google/', SignInWithOauth2APIView.as_view(), name='google_login'),

    path('following/', FollowListCreateAPIVIew.as_view(), name='follow_create'),
    path('followers/', FollowersListAPIVIew.as_view(), name='followers_api'),

    path('followers-following/<str:username>/', FollowersFollowingView.as_view(), name='followers_following'),

    path('followers-following-detail/', FollowersFollowingDetailView.as_view(), name='followers_following_detail'),

    path('profile', ProfileUpdateAPIView.as_view(), name='profile_retrieve_update'),

    path("search-history/", SearchHistoryView.as_view(), name="searches"),
    path("search/<str:username>/", SearchUserView.as_view(), name="user_search"),
    path("search/save/<str:username>/", SearchUserSaveView.as_view(), name="search_save"),
    path("search-history/<int:pk>/", SearchHistoryDeleteDestroyView.as_view(), name="search-delete"),

    path('email-verify/', EmailSignUpView.as_view(), name="email-verify")

]
