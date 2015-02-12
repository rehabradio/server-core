# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_players', '0002_auto_20150212_1212'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'verbose_name': b'Player'},
        ),
        migrations.AddField(
            model_name='player',
            name='owner',
            field=models.CharField(default=b'', max_length=500),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='player',
            name='active',
        ),
    ]
