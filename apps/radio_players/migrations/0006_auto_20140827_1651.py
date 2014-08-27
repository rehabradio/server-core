# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_players', '0005_player_owner'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=None,
        ),
    ]
