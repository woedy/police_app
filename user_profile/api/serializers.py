from django.contrib.auth import get_user_model
from rest_framework import serializers

from user_profile.models import PersonalInfo

User = get_user_model()


class UserPersonalInfoSerializers(serializers.ModelSerializer):


    class Meta:
        model = PersonalInfo
        fields = [
            'photo',
            'phone',
            "language",


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


