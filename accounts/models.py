from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from police_app_pro.utils import unique_user_id_generator


class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, last_name=None, first_name=None, password=None, is_active=True,
                    is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj


    def create_staffuser(self, email, full_name=None, last_name=None, first_name=None, password=None, ):
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
            is_staff=True
        )
        return user


    def create_superuser(self, email, full_name=None, last_name=None, first_name=None, password=None, ):
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
            is_staff=True,
            is_admin=True
        )
        return user

    def search(self, query=None):
        qs = self.get_queryset()

        if query is not None:
            or_lookup = (Q(email__icontains=query) | Q(full_name__icontains=query))

            qs = qs.filter(or_lookup).distinct()
        return qs


USER_TYPE_CHOICES = (
    ("Admin", "Admin"),
    ("User", "User"),
    ("Police", "Police"),
)

# Create your models here.
class User(AbstractBaseUser):
    user_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(default='User', choices=USER_TYPE_CHOICES, max_length=255)

    fcm_token = models.TextField(blank=True, null=True)

    email_token = models.CharField(max_length=10, blank=True, null=True)
    email_verified = models.BooleanField(default=False)

    otp_code = models.CharField(max_length=10, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    first_login = models.BooleanField(default=True)

    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin




@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

def pre_save_user_id_receiver(sender, instance, *args, **kwargs):
    if not instance.user_id:
        instance.user_id = unique_user_id_generator(instance)

pre_save.connect(pre_save_user_id_receiver, sender=User)