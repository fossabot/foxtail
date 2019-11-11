# Generated by Django 2.2.7 on 2019-11-10 03:03

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='100 characters or fewer.', max_length=100)),
                ('subtitle', models.CharField(blank=True, default='', help_text='100 characters or fewer. Optional.', max_length=100)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('show_in_menu', models.BooleanField(default=True, help_text='Set this if you want the page to be listed in site navigation.')),
                ('slug', models.SlugField(help_text='Changing this value after inital creation will break existing page URLs. Must be unique.', unique=True)),
                ('body', markdownx.models.MarkdownxField()),
            ],
            options={
                'ordering': ['sort_order'],
            },
        ),
    ]