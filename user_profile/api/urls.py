from django.urls import path

from user_profile.api.views import get_user_profile_view, update_user_profile_view, get_all_users_admin, \
    get_user_detail_admin

app_name = 'user_profile'

urlpatterns = [
    path('display-user-profile/', get_user_profile_view, name="get_user_profile_view"),
    path('update-user-profile/', update_user_profile_view, name="update_user_profile_view"),

    path('admin/get-all-users/', get_all_users_admin, name="get_all_users_admin"),
    path('admin/get-user-details/', get_user_detail_admin, name="get_user_detail_admin"),
]
