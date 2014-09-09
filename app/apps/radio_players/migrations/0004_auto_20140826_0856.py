# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radio_players', '0003_auto_20140813_1009'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='auth_token',
            new_name='token',
        ),
    ]
