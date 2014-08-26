# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_playlists', '0004_auto_20140811_0915'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='playlist',
            options={'ordering': (b'name',)},
        ),
    ]
