# Generated by Django 4.2.4 on 2023-08-27 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("communications", "0002_emailmessage"),
    ]

    operations = [
        migrations.RenameField(
            model_name="emailmessage",
            old_name="users",
            new_name="user",
        ),
    ]
