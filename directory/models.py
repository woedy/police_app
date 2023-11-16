import os
import random

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_save

from police_app_pro.utils import unique_directory_id_generator
from user_profile.models import get_default_profile_image

# Create your models here.
User = get_user_model()


def get_file_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_directory_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "directory/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class Directory(models.Model):
    directory_id = models.CharField(max_length=120, unique=True, blank=True, null=True)

    name = models.CharField(max_length=1000, null=True, blank=True)

    photo = models.ImageField(upload_to=upload_directory_path, null=True, blank=True, default=get_default_profile_image)

    following = models.ManyToManyField(User, blank=True, related_name='directory_followers')
    followers = models.ManyToManyField(User, blank=True, related_name='directory_following')

    location_name = models.CharField(max_length=200, null=True, blank=True)
    lat = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    lng = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)

    active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def post_save_directory_photo(sender, instance, *args, **kwargs):
    if not instance.photo:
        instance.photo = get_default_profile_image()

post_save.connect(post_save_directory_photo, sender=Directory)


def pre_save_directory_id_receiver(sender, instance, *args, **kwargs):
    if not instance.directory_id:
        instance.directory_id = unique_directory_id_generator(instance)

pre_save.connect(pre_save_directory_id_receiver, sender=Directory)




class DirectoryReview(models.Model):
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, related_name="directory_reviews")

    title = models.CharField(max_length=1000, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    average_rating = models.IntegerField(default=0, null=True, blank=True)

    active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
