# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('radio_queue', '0010_auto_20140826_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=500)),
                ('location', models.CharField(max_length=500)),
                ('token', models.CharField(max_length=500)),
                ('active', models.BooleanField(default=False)),
                ('queue', models.ForeignKey(to='radio_queue.Queue', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
    ]
