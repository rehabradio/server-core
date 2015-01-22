# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_metadata', '0010_auto_20150122_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='track_number',
            field=models.IntegerField(null=True),
        ),
    ]
