# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_metadata', '0002_auto_20140801_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='vote_count',
        ),
    ]
