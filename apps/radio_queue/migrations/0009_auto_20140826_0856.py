# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_queue', '0008_auto_20140811_0915'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='queue',
            options={'ordering': (b'name',)},
        ),
    ]
