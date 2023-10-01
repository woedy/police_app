from django.urls import path

from accounts.api.views import UserLogin, user_registration_view, verify_user_email, PasswordResetView, \
    confirm_otp_password_view, resend_email_verification, resend_password_otp, new_password_reset_view
from communications.api.views import send_email_message

app_name = 'communications'

urlpatterns = [
    # CLIENT URLS
    path('send-email-message/', send_email_message, name="send_email_message"),
  ]