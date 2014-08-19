# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_queue', '0006_queuetrackhistory_queue'),
    ]

    operations = [
        migrations.AddField(
            model_name='queuetrack',
            name='created',
            field=models.DateTimeField(default='2014-08-01T11:37:47.203Z', auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='queuetrack',
            name='queue',
            field=models.ForeignKey(default=1, to='radio_queue.Queue'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='queuetrack',
            name='updated',
            field=models.DateTimeField(default='2014-08-01T11:37:47.203Z', auto_now=True),
            preserve_default=True,
        ),
    ]
