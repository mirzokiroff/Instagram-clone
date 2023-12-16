# views.py
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationViewSet(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        queryset = Notification.objects.all()

        if current_user:
            queryset = queryset.filter(owner=current_user.id)
            queryset.update(is_read=True)
        return queryset
