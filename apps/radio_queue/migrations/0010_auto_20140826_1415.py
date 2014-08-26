# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_queue', '0009_auto_20140826_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='queuetrack',
            name='state',
            field=models.CharField(max_length=500, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='queuetrack',
            name='time_position',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
