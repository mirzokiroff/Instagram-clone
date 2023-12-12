from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationViewSet(APIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Retrieve unread notifications
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        serializer = NotificationSerializer(notifications, many=True)

        # Mark retrieved notifications as read
        notifications.update(is_read=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
