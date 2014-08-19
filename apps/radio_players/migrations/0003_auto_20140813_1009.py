# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_players', '0002_auto_20140813_0846'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([(b'queue', b'active')]),
        ),
    ]
