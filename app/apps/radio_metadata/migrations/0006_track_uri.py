# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_metadata', '0005_auto_20140808_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='uri',
            field=models.CharField(default='test:uri', max_length=500),
            preserve_default=False,
        ),
    ]
