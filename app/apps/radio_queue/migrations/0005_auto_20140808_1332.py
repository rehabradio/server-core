# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('radio_metadata', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('radio_queue', '0004_auto_20140808_1303'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueueTrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveIntegerField(null=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('track', models.ForeignKey(to='radio_metadata.Track')),
            ],
            options={
                'ordering': (b'position',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QueueTrackHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('track', models.ForeignKey(to='radio_metadata.Track')),
            ],
            options={
                'ordering': (b'created',),
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='queuedtrack',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='queuedtrack',
            name='track',
        ),
        migrations.DeleteModel(
            name='QueuedTrack',
        ),
        migrations.RemoveField(
            model_name='queuedtrackhistory',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='queuedtrackhistory',
            name='track',
        ),
        migrations.DeleteModel(
            name='QueuedTrackHistory',
        ),
    ]
