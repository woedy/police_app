from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.response import Response

from dashboard.api.serializers import DashOverviewSerializer, DashUpdatesSerializer, DirectorySerializer, \
    DirectoryReviewSerializer
from directory.models import Directory, DirectoryReview
from reports.models import Report


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_user_dashboard(request):
    payload = {}
    data = {}
    user_data = {}

    reports = Report.objects.all().order_by('-created_at')


    #Overview

    overview_serializer = DashOverviewSerializer(reports, many=True)
    if overview_serializer:
        _overview = overview_serializer.data
        data['overview'] = _overview


    #Updates

    updates = Report.objects.all().order_by('-created_at')
    updates_serializer = DashUpdatesSerializer(updates, many=True)
    if updates_serializer:
        _updates = updates_serializer.data
        data['updates'] = _updates


    #Directory
    directory = Directory.objects.all().order_by('-created_at')
    directory_serializer = DirectorySerializer(directory, many=True)
    if directory_serializer:
        _directory = directory_serializer.data
        data['directory'] = _directory

    # Reviews
    reviews = DirectoryReview.objects.all().order_by('-created_at')
    reviews_serializer = DirectoryReviewSerializer(reviews, many=True)
    if reviews_serializer:
        _reviews = reviews_serializer.data
        data['reviews'] = _reviews




    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)
