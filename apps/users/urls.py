from django.urls import path
from apps.users.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('profile/<int:pk>/', AccountViewSet.as_view(), name='profile'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('following', FollowListCreateAPIVIew.as_view()),
    path('following/<str:username>', FollowingListAPIViewByUsername.as_view()),
    path('unfollow/<str:username>', UnFollowAPIView.as_view()),
    path('followers', FollowersListAPIVIew.as_view()),
    path('followers/<str:username>', FollowersListAPIViewByUsername.as_view()),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('<str:username>', ProfileRetrieveUpdateDestroyAPIView.as_view()),
]
