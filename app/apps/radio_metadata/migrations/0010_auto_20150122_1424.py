# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_metadata', '0009_auto_20140918_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='duration_ms',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='track',
            name='preview_url',
            field=models.URLField(null=True),
        ),
    ]
