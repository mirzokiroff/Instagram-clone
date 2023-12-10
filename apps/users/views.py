from django.contrib.auth import authenticate
from django.http import Http404
from django.utils.text import slugify
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied, ValidationError
from rest_framework.generics import ListCreateAPIView, ListAPIView, \
    RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from content.models import Post
from content.serializers import PostSerializer
from users.models import UserProfile, UserSearch
from users.oauth2 import oauth2_sign_in
from users.serializers import UserProfileSerializer, RegisterSerializer, LoginSerializer, \
    UserFollowingModelSerializer, UserViewProfileModelSerializer, FollowersFollowingSerializer, \
    SignInWithOauth2Serializer, \
    SearchUserSerializer


class IsAuthenticatedAndOwner(BasePermission):
    message = 'You must be the owner of this object.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class FollowListCreateAPIVIew(ListCreateAPIView):
    serializer_class = UserFollowingModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.following.filter()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserViewProfileModelSerializer(page, many=True, context={'request': self.request})
            return self.get_paginated_response(serializer.data)

        serializer = UserViewProfileModelSerializer(queryset, many=True, context={'request': self.request})
        return Response(serializer.data)


class FollowersListAPIVIew(ListAPIView):
    serializer_class = UserViewProfileModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.followers.all()


class FollowersFollowingView(RetrieveAPIView):
    serializer_class = FollowersFollowingSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        username = self.kwargs['username']
        user_profile = UserProfile.objects.get(username=username)
        return user_profile


class FollowersFollowingDetailView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the authenticated user's profile
        user_profile = self.request.user

        # Check if the authenticated user has a profile
        if user_profile:
            # Get the user's followers and following
            followers = user_profile.followers.all()
            following = user_profile.following.all()

            # Combine followers and following to get a list of users
            users_to_include = list(followers) + list(following) + [user_profile]

            # Get posts from the users in the combined list
            return Post.objects.filter(user__in=users_to_include)

        else:
            raise Http404("User profile not found.")


class ProfileUpdateAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    parser_classes = [MultiPartParser]
    http_method_names = ('get', 'patch')
    permission_classes = [IsAuthenticated, IsAuthenticatedAndOwner]

    def get_object(self):
        user = self.request.user
        if user.is_authenticated:
            return user
        user = UserProfile.objects.filter(username=slugify(self.kwargs['username']))
        if user:
            return user.first()
        raise Http404

    def update(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user != self.get_object():
                raise PermissionDenied()
            partial = kwargs.pop('partial', False)
            instance = request.user
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            instance.set_password(instance.password)
            instance.save()

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        raise NotAuthenticated()


class RegisterView(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        # confirm_password = request.data.get("confirm_password")
        user = authenticate(username=username, password=password)  # confirm_password=confirm_password) # noqa
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({"refresh": str(refresh), "access": str(refresh.access_token)})  # noqa
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class SignInWithOauth2APIView(CreateAPIView):
    serializer_class = SignInWithOauth2Serializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = SignInWithOauth2Serializer(data=request.data)
        data = request.data

        if serializer.is_valid():
            user = serializer.validated_data
            if token := data.get('token'):
                return Response(oauth2_sign_in(token))
            return Response({'message': 'You have successfully signed in', 'user_id': user.token})
        raise ValidationError('token is missing or invalid')


class SearchUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        search_query = self.kwargs.get('username')
        # Use a valid lookup type for filtering (e.g., 'icontains' for case-insensitive containment)
        queryset = UserProfile.objects.filter(username__icontains=search_query)
        serializer = UserProfileSerializer(queryset, many=True)
        search_data = UserSearch.objects.filter(search=search_query, user=request.user)
        if search_data:
            search_data.delete()
        user = UserSearch.objects.create(search=search_query, user=request.user)
        user.save()
        user.refresh_from_db()
        return Response(serializer.data)


class SearchHistoryView(APIView):
    permission_classes = [IsAuthenticated, IsAuthenticatedAndOwner]

    def get(self, request, *args, **kwargs):
        queryset = UserSearch.objects.filter(user=request.user)
        serializer = SearchUserSerializer(queryset, many=True)
        return Response(serializer.data)


class SearchHistoryDeleteDestroyView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            user_search_id = kwargs.get('pk')
            user_search = UserSearch.objects.get(id=user_search_id, user=request.user)
            if user_search:
                user_search.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserSearch.DoesNotExist:
            return Response({"error": "Search history entry not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
