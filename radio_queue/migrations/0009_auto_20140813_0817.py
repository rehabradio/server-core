# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_queue', '0008_auto_20140811_0915'),
        ('radio_players', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='player',
            field=models.ForeignKey(to='radio_players.Player', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='queue',
            unique_together=set([(b'id', b'player')]),
        ),
    ]
