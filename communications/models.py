import os
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_message_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "messages/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class PrivateChatRoom(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='chat_user1', null=True,
                              blank=True)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='chat_user2', null=True,
                              blank=True)

    connected_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="connected_users")
    is_active = models.BooleanField(default=False)

    def connect_user(self, user):
        is_user_added = False
        if not user is self.connected_users.all():
            self.connected_users.add(user)
            is_user_added = True
        return is_user_added

    def disconnect_user(self, user):
        is_user_removed = False
        if user in self.connected_users.all():
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
        return f"PrivateChatRoom-{self.id}"


class RoomChatMessageManager(models.Manager):
    def by_room(self, room):
        qs = PrivateRoomChatMessage.objects.filter(room=room).order_by("-timestamp")
        return qs


class PrivateRoomChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE, related_name="private_chat_room_messages")
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(unique=False, blank=False)
    read = models.BooleanField(default=False)


    objects = RoomChatMessageManager()

    def __str__(self):
        return self.message



class PrivateRoomChatImage(models.Model):
    message = models.ForeignKey(PrivateRoomChatMessage, on_delete=models.CASCADE, related_name="private_chat_room_message")
    image = models.ImageField(upload_to=upload_message_image_path, null=True, blank=True)






class EmailMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_email_message")

    name = models.CharField(max_length=255, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
