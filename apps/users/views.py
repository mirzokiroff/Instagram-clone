from django.http import Http404
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.generics import ListCreateAPIView, ListAPIView, \
    RetrieveUpdateDestroyAPIView, CreateAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from shared.permissions import IsPublicAccount
from apps.users.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from apps.users.serializers import UserProfileSerializer
from django.utils.text import slugify


class AccountViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, ]
    parser_classes = [MultiPartParser, ]
    http_method_names = ('get', 'get_id', 'patch')


class UserDetailView(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    http_method_names = ('get', 'patch')


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
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({"refresh": str(refresh), "access": str(refresh.access_token)}) # noqa
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class FollowListCreateAPIVIew(ListCreateAPIView):
    serializer_class = UserFollowingModelSerializer
    permission_classes = (IsAuthenticated,)

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


# class UnFollowAPIView(DestroyAPIView):
#     queryset = UserProfile.objects.all()
#     lookup_field = 'username'
#     permission_classes = (IsAuthenticated,)
#
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         user = request.user
#         if user.following.filter(id=instance.id).first():
#             user.following.remove(instance)
#             instance.followers.remove(user)
#             instance.save()
#             user.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         raise Http404


class FollowersListAPIVIew(ListAPIView):
    serializer_class = UserViewProfileModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.followers.all()


class FollowersListAPIViewByUsername(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserViewProfileModelSerializer
    permission_classes = (IsPublicAccount, IsAuthenticated)

    def get_queryset(self):
        if username := self.kwargs.get('username'):
            qs = super().get_queryset().filter(username=username)
            if qs.exists():
                user: UserProfile = qs.first()
                return user.followers.all()
        raise Http404


class FollowingListAPIViewByUsername(FollowersListAPIViewByUsername):
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.username == self.kwargs['username']:
            return user
        user = UserProfile.objects.filter(username=slugify(self.kwargs['username']))
        if user:
            return user.all()
        raise Http404


class FollowersView(generics.RetrieveAPIView):
    serializer_class = FollowersSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        username = self.kwargs['username']
        user_profile = UserProfile.objects.get(username=username)
        return user_profile


class ProfileRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    http_method_names = ('get',)

    def get_object(self):
        user = self.request.user
        if user.is_authenticated and user.username == self.kwargs['username']:
            return user
        user = UserProfile.objects.filter(username=slugify(self.kwargs['username']))
        if user:
            return user.first()
        raise Http404

    def destroy(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user != self.get_object():
                raise PermissionDenied()
            self.perform_destroy(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise NotAuthenticated()

    def update(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user != self.get_object():
                raise PermissionDenied()
            partial = kwargs.pop('partial', False)
            instance = request.user
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        raise NotAuthenticated()
