from rest_framework import status
from rest_framework.fields import CharField, HiddenField, CurrentUserDefault
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from chat.models import Message


class MessageSerializer(ModelSerializer):
    id = CharField(read_only=True)
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'id', 'sender']

    def create(self, validated_data):
        sender: Message = validated_data['user']
        recipient: Message = validated_data['username']
        text: Message = validated_data['message']
        if recipient:
            recipient.message.add(text)
            recipient.save()
            return recipient
        else:
            return Response({"message": "recipient does not exists"}, status=status.HTTP_404_NOT_FOUND)
