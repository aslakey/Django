# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='link',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='post',
            name='published_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='text',
            field=models.TextField(default=datetime.datetime(2015, 11, 30, 23, 38, 18, 447221, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
