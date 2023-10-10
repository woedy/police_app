from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mysite.utils import base64_file
from reports.api.serializers import ReportSerializer
from reports.models import Report
from user_profile.api.serializers import AllUsersSerializers
from user_profile.models import PersonalInfo

User = get_user_model()

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_user_profile_view(request):
    payload = {}
    data = {}
    user_data = {}

    user_id = request.query_params.get('user_id', None)

    user = User.objects.get(user_id=user_id)
    personal_info = PersonalInfo.objects.get(user=user)

    user_data['user_id'] = user.user_id
    user_data['email'] = user.email
    user_data['full_name'] = user.full_name

    user_data['photo'] = personal_info.photo.url

    user_data['following'] = personal_info.following.all().count()
    user_data['followers'] = personal_info.followers.all().count()

    reports = Report.objects.all().filter(reporter=user)
    reports_serializer = ReportSerializer(reports, many=True)
    if reports_serializer:
        _reports = reports_serializer.data
        user_data['incidents_reported'] = _reports
    user_data['reports'] = reports.count()


    data['user_data'] = user_data


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)





@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def update_user_profile_view(request):
    payload = {}
    data = {}
    user_data = {}
    errors = {}

    user_id = request.data.get('user_id', '').lower()
    email = request.data.get('email', '').lower()
    full_name = request.data.get('full_name', '')
    phone = request.data.get('phone', '')
    photo = request.data.get('photo', '')

    user = User.objects.filter(user_id=user_id).first()

    if user is None:
        errors['user_id'] = ['Invalid user ID.']
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    if not email:
        errors['email'] = ['Email is required.']

    if not full_name:
        errors['full_name'] = ['Full name is required.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    #user.email = email
    user.full_name = full_name
    user.save()

    personal_info = PersonalInfo.objects.get(user=user)
    personal_info.phone = phone

    if photo:
        personal_info.photo = photo
    personal_info.save()

    data['email'] = user.email
    data['full_name'] = user.full_name
    data['photo'] = personal_info.photo.url

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_users_admin(request):
    payload = {}
    data = {}

    all_users = User.objects.all()
    all_users_serializer = AllUsersSerializers(all_users, many=True)
    if all_users_serializer:
        _all_users = all_users_serializer.data
        data['all_users'] = _all_users




    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_user_detail_admin(request):
    payload = {}
    data = {}

    user_id = request.query_params.get('user_id', None)


    user_details = User.objects.get(user_id=user_id)
    user_details_serializer = AllUsersSerializers(user_details, many=False)
    if user_details_serializer:
        _user_details = user_details_serializer.data
        data['user_details'] = _user_details




    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)
