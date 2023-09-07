from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from apps.chat.models import Message
from apps.chat.serializers import MessageSerializer


class MessageViewSet(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
