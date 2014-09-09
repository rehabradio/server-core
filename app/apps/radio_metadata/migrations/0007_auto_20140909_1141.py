# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_metadata', '0006_track_uri'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='artists',
            field=models.ManyToManyField(related_name=b'track', to=b'radio_metadata.Artist'),
        ),
    ]
