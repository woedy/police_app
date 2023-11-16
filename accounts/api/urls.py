from django.urls import path

from accounts.api.views import UserLogin, user_registration_view, verify_user_email, PasswordResetView, \
    confirm_otp_password_view, resend_email_verification, resend_password_otp, new_password_reset_view, AdminLogin, \
    add_new_user_view, admin_delete_user, admin_new_password_reset_view

app_name = 'accounts'

urlpatterns = [
    # CLIENT URLS
    path('login-user/', UserLogin.as_view(), name="login_user"),
    path('login-admin/', AdminLogin.as_view(), name="login_admin"),

    path('register-user/', user_registration_view, name="register_user"),

    path('verify-user-email/', verify_user_email, name="verify_user_email"),
    path('resend-email-verification/', resend_email_verification, name="resend_email_verification"),

    path('forgot-user-password/', PasswordResetView.as_view(), name="forgot_password"),
    path('confirm-password-otp/', confirm_otp_password_view, name="confirm_otp_password"),
    path('resend-password-otp/', resend_password_otp, name="resend_password_otp"),
    path('new-password-reset/', new_password_reset_view, name="new_password_reset_view"),
    path('admin-new-password-reset/', admin_new_password_reset_view, name="admin_new_password_reset_view"),

    path('admin/add-user/', add_new_user_view, name="add_new_user_view"),
    path('admin/delete-user/', admin_delete_user, name="admin_delete_user"),


]
