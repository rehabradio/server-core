# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_playlists', '0002_remove_playlist_protected'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='created',
            field=models.DateTimeField(default='2014-08-01T11:37:47.203Z', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playlist',
            name='updated',
            field=models.DateTimeField(default='2014-08-01T11:37:47.203Z', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playlisttrack',
            name='created',
            field=models.DateTimeField(default='2014-08-01T11:37:47.203Z', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playlisttrack',
            name='updated',
            field=models.DateTimeField(default='2014-08-01T11:37:47.203Z', auto_now=True),
            preserve_default=False,
        ),
    ]
