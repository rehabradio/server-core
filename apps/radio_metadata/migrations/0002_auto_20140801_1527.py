# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_metadata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='image_large',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='track',
            name='image_medium',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='track',
            name='image_small',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='album',
            name='image',
        ),
    ]
