import re

from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.template.loader import get_template
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from accounts.api.serializers import UserRegistrationSerializer, PasswordResetSerializer
from all_activities.models import AllActivity
from mysite.utils import generate_email_token, generate_random_otp_code
from user_profile.models import PersonalInfo

User = get_user_model()

class UserLogin(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        payload = {}
        data = {}
        errors = {}

        email_errors = []
        password_errors = []
        fcm_token_errors = []

        email = request.data.get('email', '').lower()
        password = request.data.get('password', '')
        fcm_token = request.data.get('fcm_token', '')

        if not email:
            email_errors.append('Email is required.')

        if not password:
            password_errors.append('Password is required.')

        if not fcm_token:
            fcm_token_errors.append('FCM device token is required.')

        if email_errors:
            errors['email'] = email_errors

        if password_errors:
            errors['password'] = password_errors

        if fcm_token_errors:
            errors['fcm_token'] = fcm_token_errors

        if email_errors or password_errors or fcm_token_errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        qs = User.objects.filter(email=email)
        if qs.exists():
            not_active = qs.filter(email_verified=False)
            if not_active:
                reconfirm_msg = "resend confirmation email."
                msg1 = "Please check your email to confirm your account or " + reconfirm_msg.lower()
                email_errors.append(msg1)

        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(email, password):
            password_errors.append('Invalid Credentials')

        if password_errors:
            errors['password'] = password_errors
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if not user:
            email_errors.append('Invalid Credentials')

        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

        try:
            user_personal_info = PersonalInfo.objects.get(user=user)
        except PersonalInfo.DoesNotExist:
            user_personal_info = PersonalInfo.objects.create(user=user)

        user_personal_info.active = True
        user_personal_info.save()

        user.fcm_token = fcm_token
        user.save()

        data["user_id"] = user.user_id
        data["email"] = user.email
        data["full_name"] = user.full_name
        data["token"] = token.key
        data["first_login"] = user.first_login

        payload['message'] = "Successful"
        payload['data'] = data

        new_activity = AllActivity.objects.create(
            user=user,
            subject="User Login",
            body=user.email + " Just logged in."
        )
        new_activity.save()

        if user.first_login is True:
            user.first_login = False
            user.save()

        return Response(payload, status=status.HTTP_200_OK)


class AdminLogin(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        payload = {}
        data = {}
        errors = {}

        email_errors = []
        password_errors = []
        fcm_token_errors = []

        email = request.data.get('email', '').lower()
        password = request.data.get('password', '')
        fcm_token = request.data.get('fcm_token', '')

        if not email:
            email_errors.append('Email is required.')

        if not password:
            password_errors.append('Password is required.')

        if not fcm_token:
            fcm_token_errors.append('FCM device token is required.')

        if email_errors:
            errors['email'] = email_errors

        if password_errors:
            errors['password'] = password_errors

        if fcm_token_errors:
            errors['fcm_token'] = fcm_token_errors

        if email_errors or password_errors or fcm_token_errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        qs = User.objects.filter(email=email)
        if qs.exists():
            not_active = qs.filter(email_verified=False)
            if not_active:
                reconfirm_msg = "resend confirmation email."
                msg1 = "Please check your email to confirm your account or " + reconfirm_msg.lower()
                email_errors.append(msg1)

            if not qs.first().admin:
                email_errors.append('The user is not an admin')

        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(email, password):
            password_errors.append('Invalid Credentials')

        if password_errors:
            errors['password'] = password_errors
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if not user:
            email_errors.append('Invalid Credentials')

        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

        try:
            user_personal_info = PersonalInfo.objects.get(user=user)
        except PersonalInfo.DoesNotExist:
            user_personal_info = PersonalInfo.objects.create(user=user)

        user_personal_info.active = True
        user_personal_info.save()

        user.fcm_token = fcm_token
        user.save()

        data["user_id"] = user.user_id
        data["email"] = user.email
        data["full_name"] = user.full_name
        data["token"] = token.key
        data["first_login"] = user.first_login

        payload['message'] = "Successful"
        payload['data'] = data

        new_activity = AllActivity.objects.create(
            user=user,
            subject="User Login",
            body=user.email + " Just logged in."
        )
        new_activity.save()

        if user.first_login is True:
            user.first_login = False
            user.save()

        return Response(payload, status=status.HTTP_200_OK)


def check_password(email, password):
    try:
        user = User.objects.get(email=email)
        return user.check_password(password)
    except User.DoesNotExist:
        return False




@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def user_registration_view(request):
    payload = {}
    data = {}
    errors = {}

    email_errors = []
    full_name_errors = []
    password_errors = []

    email = request.data.get('email', '').lower()
    full_name = request.data.get('full_name', '')
    password = request.data.get('password', '')
    password2 = request.data.get('password2', '')

    if not email:
        email_errors.append('Email is required.')

    if not is_valid_email(email):
        email_errors.append('Valid email required.')

    if check_email_exist(email):
        email_errors.append('Email already exists in our database.')

    if not full_name:
        full_name_errors.append('Full name is required.')

    if not is_valid_full_name(full_name):
        full_name_errors.append('Full name must have more than 5 letters.')

    if not password:
        password_errors.append('Password is required.')

    if password != password2:
        password_errors.append("Passwords don't match.")

    if not is_valid_password(password):
        password_errors.append("Password must be at least 8 characters long\n- Must include at least one uppercase letter,\n- One lowercase letter, one digit,\n- And one special character")

    if email_errors:
        errors['email'] = email_errors

    if full_name_errors:
        errors['full_name'] = full_name_errors

    if password_errors:
        errors['password'] = password_errors

    if email_errors or full_name_errors or password_errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    # If no errors, proceed with registration
    # Your registration logic here

    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        data["user_id"] = user.user_id
        data["email"] = user.email
        data["full_name"] = user.full_name
        data["first_login"] = user.first_login

        personal_info = PersonalInfo.objects.create(
            user=user
        )
        personal_info.save()

    token = Token.objects.get(user=user).key
    data['token'] = token



    email_token = generate_email_token()

    user = User.objects.get(email=email)
    user.email_token = email_token
    user.save()

    context = {
        'email_token': email_token,
        'email': user.email,
        'full_name': user.full_name
    }

    txt_ = get_template("registration/emails/verify.txt").render(context)
    html_ = get_template("registration/emails/verify.html").render(context)

    subject = 'EMAIL CONFIRMATION CODE'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    sent_mail = send_mail(
        subject,
        txt_,
        from_email,
        recipient_list,
        html_message=html_,
        fail_silently=False
    )

    new_activity = AllActivity.objects.create(
        user=user,
        subject="User Registration",
        body=user.email + " Just created an account."
    )
    new_activity.save()




    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)
def check_email_exist(email):

    qs = User.objects.filter(email=email)
    if qs.exists():
        return True
    else:
        return False


def is_valid_email(email):
    # Regular expression pattern for basic email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Using re.match to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False


def is_valid_password(password):
    # Check for at least 8 characters
    if len(password) < 8:
        return False

    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False

    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False

    # Check for at least one digit
    if not re.search(r'[0-9]', password):
        return False

    # Check for at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    return True

def is_valid_full_name(name):
    # Check if the name is at least 5 characters long
    if len(name) < 5:
        return False
    return True


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def verify_user_email(request):
    payload = {}
    data = {}
    errors = {}

    email_errors = []
    token_errors = []

    email = request.data.get('email', '').lower()
    email_token = request.data.get('email_token', '')

    if not email:
        email_errors.append('Email is required.')

    qs = User.objects.filter(email=email)
    if not qs.exists():
        email_errors.append('Email does not exist.')

    if email_errors:
        errors['email'] = email_errors

    if not email_token:
        token_errors.append('Token is required.')

    user = None
    if qs.exists():
        user = qs.first()
        if email_token != user.email_token:
            token_errors.append('Invalid Token.')

    if token_errors:
        errors['email_token'] = token_errors

    if email_errors or token_errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_personal_info = PersonalInfo.objects.get(user=user)
    except PersonalInfo.DoesNotExist:
        user_personal_info = PersonalInfo.objects.create(user=user)

    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        token = Token.objects.create(user=user)

    user.is_active = True
    user.email_verified = True
    user.save()

    data["user_id"] = user.user_id
    data["email"] = user.email
    data["full_name"] = user.full_name
    data["token"] = token.key

    payload['message'] = "Successful"
    payload['data'] = data

    new_activity = AllActivity.objects.create(
        user=user,
        subject="Verify Email",
        body=user.email + " just verified their email",
    )
    new_activity.save()

    return Response(payload, status=status.HTTP_200_OK)



class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer



    def post(self, request, *args, **kwargs):
        payload = {}
        data = {}
        errors = {}
        email_errors = []

        email = request.data.get('email', '').lower()

        if not email:
            email_errors.append('Email is required.')
        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

        qs = User.objects.filter(email=email)
        if not qs.exists():
            email_errors.append('Email does not exist.')
            if email_errors:
                errors['email'] = email_errors
                payload['message'] = "Error"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_404_NOT_FOUND)


        user = User.objects.filter(email=email).first()
        otp_code = generate_random_otp_code()
        user.otp_code = otp_code
        user.save()

        context = {
            'otp_code': otp_code,
            'email': user.email,
            'full_name': user.full_name
        }

        txt_ = get_template("registration/emails/send_otp.txt").render(context)
        html_ = get_template("registration/emails/send_otp.html").render(context)

        subject = 'OTP CODE'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        sent_mail = send_mail(
            subject,
            txt_,
            from_email,
            recipient_list,
            html_message=html_,
            fail_silently=False
        )
        data["otp_code"] = otp_code
        data["email"] = user.email
        data["user_id"] = user.user_id

        new_activity = AllActivity.objects.create(
            user=user,
            subject="Reset Password",
            body="OTP sent to " + user.email,
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

        return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def confirm_otp_password_view(request):
    payload = {}
    data = {}
    errors = {}

    email_errors = []
    otp_errors = []

    email = request.data.get('email', '').lower()
    otp_code = request.data.get('otp_code', '')

    if not email:
        email_errors.append('Email is required.')

    if not otp_code:
        otp_errors.append('OTP code is required.')

    user = User.objects.filter(email=email).first()

    if user is None:
        email_errors.append('Email does not exist.')

    client_otp = user.otp_code if user else ''

    if client_otp != otp_code:
        otp_errors.append('Invalid Code.')

    if email_errors or otp_errors:
        errors['email'] = email_errors
        errors['otp_code'] = otp_errors
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    data['email'] = user.email if user else ''
    data['user_id'] = user.user_id if user else ''

    payload['message'] = "Successful"
    payload['data'] = data
    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([AllowAny])
@authentication_classes([])
def resend_email_verification(request):
    payload = {}
    data = {}
    errors = {}
    email_errors = []


    email = request.data.get('email', '').lower()

    if not email:
        email_errors.append('Email is required.')
    if email_errors:
        errors['email'] = email_errors
        payload['message'] = "Error"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_404_NOT_FOUND)

    qs = User.objects.filter(email=email)
    if not qs.exists():
        email_errors.append('Email does not exist.')
        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.filter(email=email).first()
    otp_code = generate_email_token()
    user.email_token = otp_code
    user.save()

    context = {
        'email_token': otp_code,
        'email': user.email,
        'full_name': user.full_name
    }

    txt_ = get_template("registration/emails/verify.txt").render(context)
    html_ = get_template("registration/emails/verify.html").render(context)

    subject = 'OTP CODE'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    sent_mail = send_mail(
        subject,
        txt_,
        from_email,
        recipient_list,
        html_message=html_,
        fail_silently=False
    )
    data["otp_code"] = otp_code
    data["emai"] = user.email
    data["user_id"] = user.user_id

    new_activity = AllActivity.objects.create(
        user=user,
        subject="Email verification sent",
        body="Email verification sent to " + user.email,
    )
    new_activity.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([AllowAny])
@authentication_classes([])
def resend_password_otp(request):
    payload = {}
    data = {}
    errors = {}
    email_errors = []


    email = request.data.get('email', '').lower()

    if not email:
        email_errors.append('Email is required.')
    if email_errors:
        errors['email'] = email_errors
        payload['message'] = "Error"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_404_NOT_FOUND)

    qs = User.objects.filter(email=email)
    if not qs.exists():
        email_errors.append('Email does not exist.')
        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.filter(email=email).first()
    otp_code = generate_random_otp_code()
    user.otp_code = otp_code
    user.save()

    context = {
        'otp_code': otp_code,
        'email': user.email,
        'full_name': user.full_name
    }

    txt_ = get_template("registration/emails/send_otp.txt").render(context)
    html_ = get_template("registration/emails/send_otp.html").render(context)

    subject = 'OTP CODE'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    sent_mail = send_mail(
        subject,
        txt_,
        from_email,
        recipient_list,
        html_message=html_,
        fail_silently=False
    )
    data["otp_code"] = otp_code
    data["emai"] = user.email
    data["user_id"] = user.user_id

    new_activity = AllActivity.objects.create(
        user=user,
        subject="Password OTP sent",
        body="Password OTP sent to " + user.email,
    )
    new_activity.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([AllowAny])
@authentication_classes([])
def new_password_reset_view(request):
    payload = {}
    data = {}
    errors = {}
    email_errors = []
    password_errors = []

    email = request.data.get('email', '0').lower()
    new_password = request.data.get('new_password')
    new_password2 = request.data.get('new_password2')



    if not email:
        email_errors.append('Email is required.')
        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

    qs = User.objects.filter(email=email)
    if not qs.exists():
        email_errors.append('Email does not exists.')
        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)


    if not new_password:
        password_errors.append('Password required.')
        if password_errors:
            errors['password'] = password_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)


    if new_password != new_password2:
        password_errors.append('Password don\'t match.')
        if password_errors:
            errors['password'] = password_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.filter(email=email).first()
    user.set_password(new_password)
    user.save()

    data['email'] = user.email
    data['user_id'] = user.user_id


    payload['message'] = "Successful, Password reset successfully."
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

