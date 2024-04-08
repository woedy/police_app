from django.contrib.auth import get_user_model
from rest_framework import serializers

from reports.models import Report, LiveReport, LiveReportComment, ReportImage, ReportVideo, Officer
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
            'user_id',
            'email',
            'full_name',
            'personal_info'
        ]

class ReporterImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportImage
        fields = [
            'image',

        ]

class ReporterVideosSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportVideo
        fields = [
            'video'
        ]


class ReportSerializer(serializers.ModelSerializer):
    report_images = ReporterImagesSerializer(many=True)
    report_videos = ReporterVideosSerializer(many=True)

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

            'location_name',
            'lat',
            'lng',


        ]



class LiveReportCommentSerializer(serializers.ModelSerializer):
    user = ReporterSerializer(many=False)
    class Meta:
        model = LiveReportComment
        fields = [
            'comment',
            'user',

        ]
class LiveReportSerializer(serializers.ModelSerializer):
    live_report_comments = LiveReportCommentSerializer(many=True)

    class Meta:
        model = LiveReport
        fields = [
            'live_report_id',
            'stream_id',
            'call_id',
            'video_url',
            'video',
            'caption',
            'location_name',
            'lat',
            'lng',
            'reporter',
            'shares',
            'watched',
            'live_report_comments',
        ]


class ReportIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = [
            'report_id',
        ]


class OfficerSerializer(serializers.ModelSerializer):
    report = ReportIDSerializer(many=False)
    class Meta:
        model = Officer
        fields = [
            'id',
            'report',
            'name',
            'image',
            'police_station_location',
            'police_station_location',
            'notes',

        ]