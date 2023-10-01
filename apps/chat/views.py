from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from chat.models import Message
from chat.serializers import MessageSerializer


class MessageViewSet(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
