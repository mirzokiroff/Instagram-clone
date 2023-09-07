from rest_framework.permissions import BasePermission

from apps.users.models import UserProfile


class IsPublicAccount(BasePermission):
    def has_permission(self, request, view):
        try:
            kwargs = request.parser_context['kwargs']
            if username := kwargs.get('username'):
                user = UserProfile.objects.filter(username=username)
                if user.exists():
                    return user.first().is_public
        except KeyError:
            return False
        return False