# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_queue', '0005_auto_20140808_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='queuetrackhistory',
            name='queue',
            field=models.ForeignKey(default=1, to='radio_queue.Queue'),
            preserve_default=False,
        ),
    ]
