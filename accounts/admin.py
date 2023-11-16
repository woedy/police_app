from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from accounts.forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

# Register your models here.
class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('id', 'user_id', 'email', 'full_name', 'otp_code', 'email_token', 'email_verified', 'admin', 'is_deleted', )
    list_filter = ('admin', 'staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'full_name','fcm_token', 'otp_code', 'email_token', 'email_verified', 'is_deleted', 'password')}),
        # ('Full name', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'staff', 'is_active',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

    search_fields = ('email', 'full_name',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)

admin.site.unregister(Group)


