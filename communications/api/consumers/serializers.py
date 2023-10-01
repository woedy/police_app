from rest_framework import serializers

from communications.models import PrivateRoomChatMessage


class PrivateRoomChatMessageSerializer(serializers.ModelSerializer):


    class Meta:
        model = PrivateRoomChatMessage
        fields = ['id','room', 'message', 'timestamp', 'read' ]