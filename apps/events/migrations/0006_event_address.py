# Generated by Django 3.0.2 on 2020-01-28 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_event_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='address',
            field=models.TextField(blank=True),
        ),
    ]