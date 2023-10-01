# Generated by Django 4.2.4 on 2023-08-09 20:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Directory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "directory_id",
                    models.CharField(
                        blank=True, max_length=120, null=True, unique=True
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=1000, null=True)),
                (
                    "location_name",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "lat",
                    models.DecimalField(
                        blank=True, decimal_places=15, max_digits=30, null=True
                    ),
                ),
                (
                    "lng",
                    models.DecimalField(
                        blank=True, decimal_places=15, max_digits=30, null=True
                    ),
                ),
                ("active", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "followers",
                    models.ManyToManyField(
                        blank=True,
                        related_name="directory_following",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "following",
                    models.ManyToManyField(
                        blank=True,
                        related_name="directory_followers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DirectoryReview",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=1000, null=True)),
                ("note", models.TextField(blank=True, null=True)),
                (
                    "average_rating",
                    models.IntegerField(blank=True, default=0, null=True),
                ),
                ("active", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "directory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="directory_reviews",
                        to="directory.directory",
                    ),
                ),
            ],
        ),
    ]
