# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_players', '0019_auto_20150212_1657'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'verbose_name': b'Player'},
        ),
    ]