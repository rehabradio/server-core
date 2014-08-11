# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_playlists', '0003_auto_20140808_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlisttrack',
            name='position',
            field=models.PositiveIntegerField(),
        ),
    ]
