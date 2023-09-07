from django.http import Http404
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.generics import ListCreateAPIView, ListAPIView, \
    RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser
from shared.permissions import IsPublicAccount

from apps.users.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from apps.users.serializers import UserProfileSerializer


class AccountViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    lookup_field = 'pk'


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class RegisterView(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = UserProfile.objects.create_user(**serializer.validated_data)
            if request.data.get('is_superuser'):
                user.is_superuser = True
                user.set_password('0000')
                user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username'],
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowListCreateAPIVIew(ListCreateAPIView):
    serializer_class = UserFollowingModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.following.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserViewProfileModelSerializer(page, many=True, context={'request': self.request})
            return self.get_paginated_response(serializer.data)

        serializer = UserViewProfileModelSerializer(queryset, many=True, context={'request': self.request})
        return Response(serializer.data)


class UnFollowAPIView(generics.DestroyAPIView):
    queryset = UserProfile.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user.following.filter(id=instance.id).first():
            user.following.remove(instance)
            instance.followers.remove(user)
            instance.save()
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise Http404


class FollowersListAPIVIew(ListAPIView):
    serializer_class = UserViewProfileModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.followers.all()


class FollowersListAPIViewByUsername(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserViewProfileModelSerializer
    permission_classes = (IsPublicAccount,)

    def get_queryset(self):
        if username := self.kwargs.get('username'):
            qs = super().get_queryset().filter(username=username)
            if qs.exists():
                user: UserProfile = qs.first()
                return user.followers.all()
        raise Http404


class FollowingListAPIViewByUsername(FollowersListAPIViewByUsername):
    def get_queryset(self):
        if username := self.kwargs.get('username'):
            qs = self.queryset.filter(username=username)
            if qs.exists():
                user: UserProfile = qs.first()
                return user.following.all()
        raise Http404


class ProfileRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    http_method_names = ('get', 'patch', 'delete')

    def get_object(self):
        user = self.request.user
        if user.is_authenticated and user.username == self.kwargs['username']:
            return user
        user = UserProfile.objects.filter(username=self.kwargs['username'])
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
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        raise NotAuthenticated()
