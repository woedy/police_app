from django.contrib.auth import get_user_model
from rest_framework import serializers

from directory.models import Directory, DirectoryReview
from reports.api.serializers import ReporterSerializer
from reports.models import Report, Officer
from user_profile.models import PersonalInfo

User = get_user_model()

class ReportOfficerSerializer(serializers.ModelSerializer):


    class Meta:
        model = Officer
        fields = [
            "id",
            "name",
            "image"
        ]




class DashOverviewSerializer(serializers.ModelSerializer):
    officers = ReportOfficerSerializer(many=True)
    reporter = ReporterSerializer(many=False)



    class Meta:
        model = Report
        fields = [
            'report_id',
            'report_type',
            'note',
            'report_comments',
            'report_images',
            'report_videos',
            'approved',
            'officers',
            'created_at',

            'reporter'


        ]




class DashUpdatesSerializer(serializers.ModelSerializer):
    reporter = ReporterSerializer(many=False)


    class Meta:
        model = Report
        fields = [
            'report_id',
            'report_type',
            'reporter',
            'approved',
            'created_at',

        ]





class DirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = [
            'directory_id',
            'name',
            'location_name',
            'photo',
            'approved',

        ]





class DirectoryReviewSerializer(serializers.ModelSerializer):
    directory = DirectorySerializer(many=False)


    class Meta:
        model = DirectoryReview
        fields = [
            'directory',
            'title',
            'note',
            'average_rating',
            'approved',

        ]

