# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_metadata', '0007_auto_20140909_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='source_type',
            field=models.CharField(max_length=10, choices=[(b'lastfm', b'LastFM'), (b'spotify', b'Spotify'), (b'soundcloud', b'Soundcloud')]),
        ),
        migrations.AlterField(
            model_name='artist',
            name='source_type',
            field=models.CharField(max_length=10, choices=[(b'lastfm', b'LastFM'), (b'spotify', b'Spotify'), (b'soundcloud', b'Soundcloud')]),
        ),
        migrations.AlterField(
            model_name='track',
            name='source_type',
            field=models.CharField(max_length=10, choices=[(b'lastfm', b'LastFM'), (b'spotify', b'Spotify'), (b'soundcloud', b'Soundcloud')]),
        ),
    ]
