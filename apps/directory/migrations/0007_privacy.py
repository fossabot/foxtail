# Generated by Django 3.0.2 on 2020-01-20 13:16

from django.db import migrations

import apps.directory.fields


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0006_privacy_two'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='show_age',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='show_birthday',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='show_name',
        ),
        migrations.AddField(
            model_name='profile',
            name='location_privacy',
            field=apps.directory.fields.PrivacyField(),
        ),
    ]
