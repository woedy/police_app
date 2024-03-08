from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.response import Response

from dashboard.api.serializers import DirectorySerializer
from directory.models import Directory, DirectoryReview

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_directory_view(request):
    payload = {}
    data = {}
    errors = {}




    name = request.data.get('name', '')
    photo = request.data.get('photo', '')
    location_name = request.data.get('location_name', '')
    lat = request.data.get('lat', '')
    lng = request.data.get('lng', '')

    if not name:
        errors['name'] = ['Directory name Type is required.']

    if not photo:
        errors['photo'] = ['Photo is required.']

    if not location_name:
        errors['location_name'] = ['Location required.']

    if not lat:
        errors['lat'] = ['Location latitude is required.']

    if not lng:
        errors['lng'] = ['Location longitude is required.']


    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)



    new_directory = Directory.objects.create(
        name=name,
        photo=photo,
        location_name=location_name,
        lat=lat,
        lng=lng,

    )


    data['directory_id'] = new_directory.directory_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def delete_directory_view(request):
    payload = {}
    data = {}
    errors = {}

    directory_id = request.data.get('directory_id', '')


    if not directory_id:
        errors['directory_id'] = ['Directory id is required.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)



    directory = Directory.objects.get(directory_id=directory_id)
    directory.is_deleted = True
    directory.save()

    payload['message'] = "Directory deleted Successfully"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_directories_view(request):
    payload = {}
    data = {}
    user_data = {}

    directories = Directory.objects.all().filter(is_deleted=False).order_by('-created_at')

    directories_serializer = DirectorySerializer(directories, many=True)
    if directories_serializer:
        _directories = directories_serializer.data
        data['directories'] = _directories


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def review_directory_view(request):
    payload = {}
    data = {}
    errors = {}




    directory_id = request.data.get('directory_id', '')
    title = request.data.get('title', '')
    note = request.data.get('note', '')
    average_rating = request.data.get('average_rating', '')
    reviewer = request.data.get('reviewer', '')


    if not directory_id:
        errors['directory_id'] = ['Directory ID Type is required.']

    if not title:
        errors['title'] = ['Title is required.']

    if not note:
        errors['note'] = ['Note required.']

    if not average_rating:
        errors['average_rating'] = ['Rating required.']

    try:
        directory = Directory.objects.get(directory_id=directory_id)
    except Directory.DoesNotExist:
        errors['directory_id'] = ['Directory does not exist.']

    try:
        reviewer = User.objects.get(user_id=reviewer)
    except User.DoesNotExist:
        errors['reviewer'] = ['User does not exist.']



    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)



    new_directory_review = DirectoryReview.objects.create(
        directory=directory,
        title=title,
        note=note,
        average_rating=average_rating,
        reviewer=reviewer,
    )

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



