from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.response import Response

from reports.models import Report, Officer, UploadReport, UploadReportTag, RecordReport, RecordReportTag, ReportImage

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_report_view(request):
    payload = {}
    data = {}
    errors = {}

    report_type = request.data.get('report_type', '')


    images = request.FILES.getlist('images')
    # videos = request.data.get('videos', '')

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

    for image in images:
        image = ReportImage.objects.create(
            report=new_report,
            image=image
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
        #image=base64_file(image),
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
def record_report_view(request):
    payload = {}
    data = {}
    errors = {}


    #image = request.data.get('image', '')
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
        #video=base64_file(video),
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

