# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('radio_queue', '0001_initial'),
        ('auth', '0001_initial'),
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
                ('owner', models.CharField(default=b'', max_length=500)),
                ('queue', models.ForeignKey(to='radio_queue.Queue', null=True)),
            ],
            options={
                'verbose_name': b'Player',
            },
            bases=('auth.user',),
        ),
    ]
