from django.contrib.auth import get_user_model
from rest_framework import serializers

from reports.models import Report
from user_profile.models import PersonalInfo

User = get_user_model()

class ReporterPersonalSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalInfo
        fields = [
            'photo',

        ]
class ReporterSerializer(serializers.ModelSerializer):
    personal_info = ReporterPersonalSerializer(many=False)

    class Meta:
        model = User
        fields = [
            'email',
            'full_name',
            'personal_info'
        ]

class ReportSerializer(serializers.ModelSerializer):


    class Meta:
        model = Report
        fields = [
            'report_id',
            'report_type',
            'note',
            'report_comments',
            'report_images',
            'report_videos',
            'officers',
            'created_at',


        ]



