from django.contrib.auth import get_user_model
from rest_framework import serializers

from communications.models import PrivateChatRoom
from user_profile.models import PersonalInfo

User = get_user_model()

class PrivateChatRoomSerializers(serializers.ModelSerializer):


    class Meta:
        model = PrivateChatRoom
        fields = [
            'room_id',
        ]
class UserPersonalInfoSerializers(serializers.ModelSerializer):
    room = PrivateChatRoomSerializers(many=False)

    class Meta:
        model = PersonalInfo
        fields = [
            'photo',
            'phone',
            "language",
            'room'


        ]

class AllUsersSerializers(serializers.ModelSerializer):
    personal_info = UserPersonalInfoSerializers(many=False)

    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'full_name',
            'personal_info',
            'role',
            "is_active"
        ]


