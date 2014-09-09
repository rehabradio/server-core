# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_queue', '0002_queuedtrack_alive'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='queuedtrack',
            name='alive',
        ),
        migrations.AlterField(
            model_name='queuedtrackvote',
            name='value',
            field=models.IntegerField(default=0, choices=[(-1, -1), (0, 0), (1, 1)]),
        ),
    ]
