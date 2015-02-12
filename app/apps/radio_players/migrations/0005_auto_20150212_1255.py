# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_players', '0004_auto_20150212_1238'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'verbose_name': b'Player'},
        ),
        migrations.AddField(
            model_name='player',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
