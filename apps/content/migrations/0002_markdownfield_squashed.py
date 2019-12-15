# Generated by Django 2.2.8 on 2019-12-13 22:08

from django.db import migrations

import markdownfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='body',
            field=markdownfield.fields.MarkdownField(),
        ),
        migrations.AddField(
            model_name='page',
            name='body_rendered',
            field=markdownfield.fields.RenderedMarkdownField(editable=False),
        ),
    ]
