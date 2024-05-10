from django.urls import path

from dashboard.api.views import get_user_dashboard
from reports.api.views import add_report_view, upload_report_view, record_report_view, get_all_reports_view_admin, \
    admin_approve_report_view, delete_report_view, delete_upload_report_view, delete_record_report_view, \
    save_live_report_view, get_all_live_reports, add_report_officer_view, add_report_image_view, add_report_video_view, \
    get_all_officers_view_admin, delete_officer_view, get_officer_reports
from user_profile.api.views import get_user_profile_view, update_user_profile_view

app_name = 'reports'

urlpatterns = [
    path('add-report/', add_report_view, name="add_report_view"),
    path('add-report-officer/', add_report_officer_view, name="add_report_officer_view"),
    path('add-report-image/', add_report_image_view, name="add_report_image_view"),
    path('add-report-video/', add_report_video_view, name="add_report_video_view"),


    path('delete-report/', delete_report_view, name="delete_report_view"),

    path('upload-report/', upload_report_view, name="upload_report_view"),
    path('delete-upload-report/', delete_upload_report_view, name="delete_upload_report_view"),

    path('record-report/', record_report_view, name="record_report_view"),
    path('delete-record-report/', delete_record_report_view, name="delete_record_report_view"),

    path('admin/get-all-report/', get_all_reports_view_admin, name="get_all_reports_view_admin"),
    path('admin/approve-report/', admin_approve_report_view, name="admin_approve_report_view"),

    path('save-livestream/', save_live_report_view, name="save_live_report_view"),
    path('get-all-livestream/', get_all_live_reports, name="get_all_live_reports"),

    path('admin/get-all-officers/', get_all_officers_view_admin, name="get_all_officers_view_admin"),
    path('admin/get-officer-reports/', get_officer_reports, name="get_officer_reports"),
    path('admin/delete-officer/', delete_officer_view, name="delete_officer_view"),

]
