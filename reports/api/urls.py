from django.urls import path

from dashboard.api.views import get_user_dashboard
from reports.api.views import add_report_view, upload_report_view, record_report_view, get_all_reports_view_admin, \
    admin_approve_report_view, delete_report_view, delete_upload_report_view, delete_record_report_view
from user_profile.api.views import get_user_profile_view, update_user_profile_view

app_name = 'reports'

urlpatterns = [
    path('add-report/', add_report_view, name="add_report_view"),
    path('delete-report/', delete_report_view, name="delete_report_view"),

    path('upload-report/', upload_report_view, name="upload_report_view"),
    path('delete-upload-report/', delete_upload_report_view, name="delete_upload_report_view"),

    path('record-report/', record_report_view, name="record_report_view"),
    path('delete-record-report/', delete_record_report_view, name="delete_record_report_view"),

    path('admin/get-all-report/', get_all_reports_view_admin, name="get_all_reports_view_admin"),
    path('admin/approve-report/', admin_approve_report_view, name="admin_approve_report_view"),
]
