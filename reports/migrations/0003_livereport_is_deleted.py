# Generated by Django 5.0.3 on 2024-03-08 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_livereport_approved_officer_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='livereport',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]