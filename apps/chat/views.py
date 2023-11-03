from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from chat.models import Message
from chat.serializers import MessageSerializer
from users.models import UserProfile


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    http_method_names = ('get', 'post', 'delete')

    def post(self, request):
        sender = self.request.user
        recipient = UserProfile.username
        text = Message.message

        if recipient:
            recipient.add()
