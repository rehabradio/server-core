# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('radio_queue', '0007_auto_20140811_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queuetrack',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='queuetrack',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='queuetrack',
            name='position',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='queuetrack',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
