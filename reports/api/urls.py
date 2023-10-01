from django.urls import path

from dashboard.api.views import get_user_dashboard
from reports.api.views import add_report_view, upload_report_view, record_report_view
from user_profile.api.views import get_user_profile_view, update_user_profile_view

app_name = 'reports'

urlpatterns = [
    path('add-report/', add_report_view, name="add_report_view"),
    path('upload-report/', upload_report_view, name="upload_report_view"),
    path('record-report/', record_report_view, name="record_report_view"),
]
