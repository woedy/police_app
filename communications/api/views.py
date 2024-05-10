from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from communications.models import EmailMessage

User = get_user_model()
@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def send_email_message(request):
    payload = {}
    data = {}
    errors = {}


    user_id = request.data.get('user_id', '')
    name = request.data.get('name', '')
    subject = request.data.get('subject', '')
    message = request.data.get('message', '')



    if not user_id:
        errors['user_id'] = ['User ID is required.']


    if not name:
        errors['name'] = ['Name is required.']

    if not subject:
        errors['subject'] = ['Subject is required.']

    if not message:
        errors['message'] = ['Message is required.']

    user = User.objects.get(user_id=user_id)

    new_message = EmailMessage.objects.create(
        user=user,
        name=name,
        subject=subject,
        message=message
    )



    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    payload['message'] = "Successful, Message sent."
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

