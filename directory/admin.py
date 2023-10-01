from django.contrib import admin

from directory.models import Directory, DirectoryReview

# Register your models here.
admin.site.register(Directory)
admin.site.register(DirectoryReview)