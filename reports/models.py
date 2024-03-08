import os
import random

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save

from police_app_pro.utils import unique_report_id_generator, unique_upload_report_id_generator, \
    unique_record_report_id_generator, unique_live_report_id_generator

User = get_user_model()


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_report_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "report_images/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_officer_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "officers/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

def upload_report_video_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "report_videos/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_upload_report_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "upload_report_videos/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_record_report_video_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "record_report_videos/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_live_report_video_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "live_report_videos/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )




REPORT_TYPE_CHOICES = (
    ('Report an Officer', 'Report an Officer'),
    ('Report an Institution', 'Report an Institution'),
    ('Report a Crime', 'Report a Crime'),
    ('Police Reports', 'Police Reports'),
    ('Report a Warden', 'Report a Warden'),

)



#######################
### REPORTS
####################





class Report(models.Model):
    report_id = models.CharField(max_length=120, unique=True, blank=True, null=True)
    report_type = models.CharField(max_length=100, choices=REPORT_TYPE_CHOICES, blank=True, null=True)

    note = models.TextField(null=True, blank=True)

    contact_info = models.CharField(max_length=200, null=True, blank=True)
    user_contact_info = models.BooleanField(default=False)

    make_private = models.BooleanField(default=False)
    make_collaborative = models.BooleanField(default=False)

    shares = models.ManyToManyField(User, blank=True, related_name='report_shares')
    following = models.ManyToManyField(User, blank=True, related_name='report_followers')

    approved = models.BooleanField(default=False)



    location_name = models.CharField(max_length=200, null=True, blank=True)
    lat = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    lng = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter')


    active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




def pre_save_report_id_receiver(sender, instance, *args, **kwargs):
    if not instance.report_id:
        instance.report_id = unique_report_id_generator(instance)

pre_save.connect(pre_save_report_id_receiver, sender=Report)




class ReportComment(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="report_comments")
    comment = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





class ReportImage(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="report_images")
    image = models.FileField(upload_to=upload_report_image_path, null=True, blank=True)
    file_name = models.CharField(max_length=1000, null=True, blank=True)
    file_ext = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class ReportVideo(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="report_videos")
    video = models.FileField(upload_to=upload_report_video_path, null=True, blank=True)
    file_name = models.CharField(max_length=1000, null=True, blank=True)
    file_ext = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Officer(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="officers")
    name = models.CharField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to=upload_officer_image_path, null=True, blank=True)


#######################
### UPLOAD REPORT
####################

class UploadReport(models.Model):
    upload_report_id = models.CharField(max_length=120, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to=upload_upload_report_image_path, null=True, blank=True)

    caption = models.TextField(null=True, blank=True)

    location_name = models.CharField(max_length=200, null=True, blank=True)
    lat = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    lng = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upload_reporter')

    shares = models.ManyToManyField(User, blank=True, related_name='upload_report_shares')


    approved = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def pre_save_upload_report_id_receiver(sender, instance, *args, **kwargs):
    if not instance.upload_report_id:
        instance.upload_report_id = unique_upload_report_id_generator(instance)

pre_save.connect(pre_save_upload_report_id_receiver, sender=UploadReport)





class UploadReportTag(models.Model):
    upload_report = models.ForeignKey(UploadReport, on_delete=models.CASCADE, related_name="upload_report_tags")
    tag = models.CharField(max_length=1000, null=True, blank=True)
    x_position = models.DecimalField(default=0.0, max_digits=30, decimal_places=15, null=True, blank=True)
    y_position = models.DecimalField(default=0.0, max_digits=30, decimal_places=15, null=True, blank=True)


class UploadReportComment(models.Model):
    upload_report = models.ForeignKey(UploadReport, on_delete=models.CASCADE, related_name="upload_report_comments")
    comment = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





#######################
### RECORD REPORT
####################


class RecordReport(models.Model):
    record_report_id = models.CharField(max_length=120, unique=True, blank=True, null=True)
    video = models.FileField(upload_to=upload_record_report_video_path, null=True, blank=True)

    caption = models.TextField(null=True, blank=True)

    location_name = models.CharField(max_length=200, null=True, blank=True)
    lat = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    lng = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='record_reporter')

    shares = models.ManyToManyField(User, blank=True, related_name='record_report_shares')

    approved = models.BooleanField(default=False)


    active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def pre_save_record_report_id_receiver(sender, instance, *args, **kwargs):
    if not instance.record_report_id:
        instance.record_report_id = unique_record_report_id_generator(instance)

pre_save.connect(pre_save_record_report_id_receiver, sender=RecordReport)





class RecordReportTag(models.Model):
    record_report = models.ForeignKey(RecordReport, on_delete=models.CASCADE, related_name="record_report_tags")
    tag = models.CharField(max_length=1000, null=True, blank=True)
    x_position = models.DecimalField(default=0.0, max_digits=30, decimal_places=15, null=True, blank=True)
    y_position = models.DecimalField(default=0.0, max_digits=30, decimal_places=15, null=True, blank=True)


class RecordReportComment(models.Model):
    record_report = models.ForeignKey(RecordReport, on_delete=models.CASCADE, related_name="record_report_comments")
    comment = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




#######################
### LIVE REPORT
####################
class LiveReport(models.Model):
    live_report_id = models.CharField(max_length=120, unique=True, blank=True, null=True)
    video = models.FileField(upload_to=upload_live_report_video_path, null=True, blank=True)

    caption = models.TextField(null=True, blank=True)

    location_name = models.CharField(max_length=200, null=True, blank=True)
    lat = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    lng = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='live_reporter')

    approved = models.BooleanField(default=False)


    shares = models.ManyToManyField(User, blank=True, related_name='live_report_shares')
    watched = models.ManyToManyField(User, blank=True, related_name='live_watched_users')
    watch_count = models.IntegerField(default=0, null=True, blank=True)

    is_deleted = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def pre_save_live_report_id_receiver(sender, instance, *args, **kwargs):
    if not instance.live_report_id:
        instance.live_report_id = unique_live_report_id_generator(instance)

pre_save.connect(pre_save_live_report_id_receiver, sender=LiveReport)



class LiveReportComment(models.Model):
    live_report = models.ForeignKey(LiveReport, on_delete=models.CASCADE, related_name="live_report_comments")
    comment = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)