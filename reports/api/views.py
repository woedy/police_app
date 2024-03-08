from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.response import Response

from dashboard.api.serializers import DashUpdatesSerializer, DirectorySerializer, DirectoryReviewSerializer, \
    DashOverviewSerializer
from directory.models import Directory, DirectoryReview
from reports.api.serializers import LiveReportSerializer
from reports.models import Report, Officer, UploadReport, UploadReportTag, RecordReport, RecordReportTag, ReportImage, \
    ReportVideo, LiveReport, LiveReportComment

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_report_view(request):
    payload = {}
    data = {}
    errors = {}

    report_type = request.data.get('report_type', '')


    images = request.data.get('images', [])
    videos = request.data.get('videos', [])

    officers = request.data.get('officers', '')
    location_name = request.data.get('location_name', '')
    note = request.data.get('note', '')
    user_contact_info = request.data.get('user_contact_info', '')
    contact_info = request.data.get('contact_info', '')
    make_private = request.data.get('make_private', '')
    make_collaborative = request.data.get('make_collaborative', '')
    reporter = request.data.get('reporter', '')

    if not report_type:
        errors['report_type'] = ['Report Type is required.']

    if not officers:
        errors['officers'] = ['Officers are required.']

    if not location_name:
        errors['location_name'] = ['Location required.']

    if not note:
        errors['note'] = ['Note is required.']

    if not reporter:
        errors['reporter'] = ['Reporter is required.']


    if not user_contact_info:
        errors['user_contact_info'] = ['User contact start is required.']

    if not make_private:
        errors['make_private'] = ['Make private is required.']

    if not make_collaborative:
        errors['make_collaborative'] = ['Make collaborative is required.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    the_reporter = User.objects.get(user_id=reporter)

    new_report = Report.objects.create(
        report_type=report_type,
        note=note,
        contact_info=contact_info,
        user_contact_info=user_contact_info,
        make_private=make_private,
        make_collaborative=make_collaborative,
        location_name=location_name,
        reporter=the_reporter

    )

    print(images)

    for image in images:
        image = ReportImage.objects.create(
            report=new_report,
            image=image
        )
        # print(image)

    for video in videos:
        video = ReportVideo.objects.create(
            report=new_report,
            video=video
        )
        # print(image)


    for officer in officers:

        print(officer)
        officer = Officer.objects.create(
            report=new_report,
            name=officer
        )



    data['report_id'] = new_report.report_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def delete_report_view(request):
    payload = {}
    data = {}
    errors = {}

    report_id = request.data.get('report_id', '')


    if not report_id:
        errors['report_id'] = ['Report id is required.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)



    report = Report.objects.get(report_id=report_id)
    report.is_deleted = True
    report.save()

    payload['message'] = "Report deleted Successfully"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def upload_report_view(request):
    payload = {}
    data = {}
    errors = {}


    image = request.data.get('image', '')
    # video = request.data.get('video', '')

    caption = request.data.get('caption', '')
    location_name = request.data.get('location_name', '')
    reporter = request.data.get('reporter', '')

    tags = request.data.get('tags', '')


    if not caption:
        errors['caption'] = ['Caption is required.']

    if not location_name:
        errors['location_name'] = ['Location required.']


    if not image:
        errors['image'] = ['Image required.']



    if not reporter:
        errors['reporter'] = ['Reporter is required.']



    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    the_reporter = User.objects.get(user_id=reporter)

    new_upload_report = UploadReport.objects.create(
        image=image,
        caption=caption,
        location_name=location_name,
        reporter=the_reporter

    )


    for tag in tags:
        new_tag = UploadReportTag.objects.create(
            upload_report=new_upload_report,
            tag=tag['tag'],
            x_position=tag['x_position'],
            y_position=tag['y_position']
        )




    data['upload_report_id'] = new_upload_report.upload_report_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def delete_upload_report_view(request):
    payload = {}
    data = {}
    errors = {}

    upload_report_id = request.data.get('upload_report_id', '')

    if not upload_report_id:
        errors['upload_report_id'] = ['Upload Report id is required.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    report = UploadReport.objects.get(upload_report_id=upload_report_id)
    report.is_deleted = True
    report.save()

    payload['message'] = "Upload Report deleted Successfully"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def record_report_view(request):
    payload = {}
    data = {}
    errors = {}


    video = request.data.get('video', '')

    caption = request.data.get('caption', '')
    location_name = request.data.get('location_name', '')
    reporter = request.data.get('reporter', '')

    tags = request.data.get('tags', '')


    if not caption:
        errors['caption'] = ['Caption is required.']

    if not location_name:
        errors['location_name'] = ['Location required.']


    if not video:
        errors['video'] = ['Video required.']



    if not reporter:
        errors['reporter'] = ['Reporter is required.']



    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    the_reporter = User.objects.get(user_id=reporter)

    new_record_report = RecordReport.objects.create(
        video=video,
        caption=caption,
        location_name=location_name,
        reporter=the_reporter

    )


    for tag in tags:
        new_tag = RecordReportTag.objects.create(
            record_report=new_record_report,
            tag=tag['tag'],
            x_position=tag['x_position'],
            y_position=tag['y_position']
        )




    data['record_report_id'] = new_record_report.record_report_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)






@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def delete_record_report_view(request):
    payload = {}
    data = {}
    errors = {}

    record_report_id = request.data.get('record_report_id', '')

    if not record_report_id:
        errors['record_report_id'] = ['Record Report id is required.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    report = RecordReport.objects.get(record_report_id=record_report_id)
    report.is_deleted = True
    report.save()

    payload['message'] = "Record Report deleted Successfully"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_reports_view_admin(request):
    payload = {}
    data = {}
    user_data = {}

    reports = Report.objects.all().filter(is_deleted=False).order_by('-created_at')

    reports_serializer = DashOverviewSerializer(reports, many=True)
    if reports_serializer:
        _reports = reports_serializer.data
        data['reports'] = _reports


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)





@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def admin_approve_report_view(request):
    payload = {}
    data = {}
    errors = {}

    report_id = request.query_params.get('report_id', None)

    if not report_id:
        errors['report_id'] = ['Report id is required.']


    report_detail = Report.objects.get(report_id=report_id)
    report_detail.approved = True
    report_detail.save()

    report_serializer = DashOverviewSerializer(report_detail, many=False)
    if report_serializer:
        _report = report_serializer.data
        data['report_detail'] = _report

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def save_live_report_view(request):
    payload = {}
    data = {}
    errors = {}

    video = request.data.get('video', '')
    caption = request.data.get('caption', '')
    location_name = request.data.get('location_name', '')
    lat = request.data.get('lat', '')
    lng = request.data.get('lng', '')
    reporter_id = request.data.get('reporter', '')

    if not caption:
        errors['caption'] = ['Caption is required.']

    if not video:
        errors['video'] = ['Video required.']

    if not reporter_id:
        errors['reporter'] = ['Reporter is required.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    try:
        the_reporter = User.objects.get(user_id=reporter_id)
    except User.DoesNotExist:
        errors['reporter'] = ['Reporter does not exist.']
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    new_live_report = LiveReport.objects.create(
        video=video,
        caption=caption,
        location_name=location_name,
        lat=lat,
        lng=lng,
        reporter=the_reporter
    )

    # Add Watchers
    for watched_user_id in request.data.get('watched', []):
        try:
            watched_user = User.objects.get(user_id=watched_user_id)
            new_live_report.watched.add(watched_user)
        except User.DoesNotExist:
            pass

    for comment_data in request.data.get('comments', []):
        try:
            commenter = User.objects.get(user_id=comment_data['user'])
            new_comment = LiveReportComment.objects.create(
                live_report=new_live_report,
                comment=comment_data['comment'],
                user=commenter
            )
        except User.DoesNotExist:
            pass

    data['live_report_id'] = new_live_report.live_report_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_live_reports(request):
    payload = {}
    data = {}
    user_data = {}

    live_reports = LiveReport.objects.all().filter(is_deleted=False).order_by('-created_at')

    live_reports_serializer = LiveReportSerializer(live_reports, many=True)
    if live_reports_serializer:
        _live_reports = live_reports_serializer.data
        data['live_reports'] = _live_reports


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

