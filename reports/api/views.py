from django.contrib.auth import get_user_model
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from dashboard.api.serializers import DashUpdatesSerializer, DirectorySerializer, DirectoryReviewSerializer, \
    DashOverviewSerializer
from directory.models import Directory, DirectoryReview
from reports.api.serializers import LiveReportSerializer, OfficerSerializer
from reports.models import Report, Officer, UploadReport, UploadReportTag, RecordReport, ReportImage, \
    ReportVideo, LiveReport, LiveReportComment

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_report_view(request):
    payload = {}
    data = {}
    errors = {}

    report_type = request.data.get('report_type', '')

    location_name = request.data.get('location_name', '')
    note = request.data.get('note', '')
    user_contact_info = request.data.get('user_contact_info', '')
    contact_info = request.data.get('contact_info', '')
    make_private = request.data.get('make_private', '')
    make_collaborative = request.data.get('make_collaborative', '')
    reporter = request.data.get('reporter', '')

    if not report_type:
        errors['report_type'] = ['Report Type is required.']


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


    try:
        the_reporter = User.objects.get(user_id=reporter)
    except:
        errors['reporter'] = ['Reporter does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)



    new_report = Report.objects.create(
        report_type=report_type,
        note=note,
        contact_info=contact_info,
        location_name=location_name,
        reporter=the_reporter

    )


    if user_contact_info == "true":
        new_report.user_contact_info = True
        new_report.save()
    elif user_contact_info == "false":
        new_report.user_contact_info = False
        new_report.save()

    if make_private == "true":
        new_report.make_private = True
        new_report.save()
    elif make_private == "false":
        new_report.make_private = False
        new_report.save()

    if make_collaborative == "true":
        new_report.make_collaborative = True
        new_report.save()
    elif make_collaborative == "false":
        new_report.make_collaborative = False
        new_report.save()


    data['report_id'] = new_report.report_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_report_officer_view(request):
    payload = {}
    data = {}
    errors = {}

    report_id = request.data.get('report_id', '')
    officer = request.data.get('officer', '')
    image = request.data.get('image', '')
    police_station_location = request.data.get('police_station_location', '')
    badge_id = request.data.get('badge_id', '')
    notes = request.data.get('notes', '')

    if not officer:
        errors['officer'] = ['Officer is required.']

    if not officer:
        errors['officer'] = ['Officer is required.']


    try:
        report = Report.objects.get(report_id=report_id)
    except:
        errors['report_id'] = ['Report does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    officer = Officer.objects.create(
        report=report,
        name=officer,
        image=image,
        police_station_location=police_station_location,
        badge_id=badge_id,
        notes=notes,
    )

    data['report_id'] = report.report_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_report_image_view(request):
    payload = {}
    data = {}
    errors = {}

    report_id = request.data.get('report_id', '')
    image = request.data.get('image', '')

    if not image:
        errors['image'] = ['Image is required.']

    try:
        report = Report.objects.get(report_id=report_id)
    except:
        errors['report_id'] = ['Report does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    image = ReportImage.objects.create(
        report=report,
        image=image
    )

    data['report_id'] = report.report_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_report_video_view(request):
    payload = {}
    data = {}
    errors = {}

    report_id = request.data.get('report_id', '')
    video = request.data.get('video', '')

    if not video:
        errors['video'] = ['Video is required.']

    try:
        report = Report.objects.get(report_id=report_id)
    except:
        errors['report_id'] = ['Report does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    image = ReportVideo.objects.create(
        report=report,
        video=video
    )

    data['report_id'] = report.report_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_report_view_previous(request):
    payload = {}
    data = {}
    errors = {}

    report_type = request.data.get('report_type', '')


    images = request.FILES.getlist('images', [])
    videos = request.FILES.getlist('videos', [])

    officers = request.data.get('officers', [])
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


    try:
        the_reporter = User.objects.get(user_id=reporter)
    except:
        errors['reporter'] = ['Reporter does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)



    new_report = Report.objects.create(
        report_type=report_type,
        note=note,
        contact_info=contact_info,
        location_name=location_name,
        reporter=the_reporter

    )


    if user_contact_info == "true":
        new_report.user_contact_info = True
        new_report.save()
    elif user_contact_info == "false":
        new_report.user_contact_info = False
        new_report.save()

    if make_private == "true":
        new_report.make_private = True
        new_report.save()
    elif make_private == "false":
        new_report.make_private = False
        new_report.save()

    if make_collaborative == "true":
        new_report.make_collaborative = True
        new_report.save()
    elif make_collaborative == "false":
        new_report.make_collaborative = False
        new_report.save()

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
@authentication_classes([CustomJWTAuthentication, ])
def add_report_view22222(request):
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
@authentication_classes([CustomJWTAuthentication, ])
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
@authentication_classes([CustomJWTAuthentication, ])
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
@authentication_classes([CustomJWTAuthentication, ])
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
@authentication_classes([CustomJWTAuthentication, ])
def delete_officer_view(request):
    payload = {}
    data = {}
    errors = {}

    id = request.data.get('id', '')

    if not id:
        errors['id'] = ['ID is required.']

    try:
        officer = Officer.objects.get(id=id)
    except:
        errors['id'] = ['officer does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    officer.delete()

    payload['message'] = "Deleted Successfully"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_officer_reports(request):
    payload = {}
    data = {}
    errors = {}

    id = request.data.get('id', '')

    if not id:
        errors['id'] = ['ID is required.']


    try:
        officer = Officer.objects.get(id=id)
    except:
        errors['id'] = ['officer does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    reports = Report.objects.filter(officers=officer)


    reports_serializer = DashOverviewSerializer(reports, many=True)
    if reports_serializer:
        _reports = reports_serializer.data
        data['reports'] = _reports




    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def record_report_view(request):
    payload = {}
    data = {}
    errors = {}


    video = request.data.get('video', '')

    caption = request.data.get('caption', '')
    location_name = request.data.get('location_name', '')
    reporter = request.data.get('reporter', '')



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


    data['record_report_id'] = new_record_report.record_report_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)






@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
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
@authentication_classes([CustomJWTAuthentication, ])
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





@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_officers_view_admin(request):
    payload = {}
    data = {}
    user_data = {}

    officers = Officer.objects.all().order_by('-id')

    officers_serializer = OfficerSerializer(officers, many=True)
    if officers_serializer:
        _officers = officers_serializer.data
        data['officers'] = _officers


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)





@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
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
@authentication_classes([CustomJWTAuthentication, ])
def save_live_report_view(request):
    payload = {}
    data = {}
    errors = {}

    stream_id = request.data.get('stream_id', '')
    call_id = request.data.get('call_id', '')
    video_url = request.data.get('video_url', '')
    video = request.data.get('video', '')

    reporter_id = request.data.get('reporter', '')


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
        stream_id=stream_id,
        call_id=call_id,
        video_url=video_url,
        video=video,
        reporter=the_reporter
    )



    data['live_report_id'] = new_live_report.live_report_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
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

