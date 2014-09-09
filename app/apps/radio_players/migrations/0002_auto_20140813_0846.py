# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_players', '0001_initial'),
        ('radio_queue', '0008_auto_20140811_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='active',
            field=models.BooleanField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='queue',
            field=models.ForeignKey(to='radio_queue.Queue', null=True),
            preserve_default=True,
        ),
    ]
