from django.urls import path

from dashboard.api.views import get_user_dashboard
from user_profile.api.views import get_user_profile_view, update_user_profile_view

app_name = 'dashboard'

urlpatterns = [
    path('user-dashboard/', get_user_dashboard, name="get_user_dashboard"),
]
