# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_playlists', '0005_auto_20140826_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='protection',
            field=models.CharField(default=b'private', max_length=10, choices=[(b'private', b'Private'), (b'public', b'Public')]),
            preserve_default=True,
        ),
    ]
