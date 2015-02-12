# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('radio_metadata', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': (b'name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QueueTrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveIntegerField()),
                ('state', models.CharField(max_length=500, null=True)),
                ('time_position', models.IntegerField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('queue', models.ForeignKey(to='radio_queue.Queue')),
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
                ('queue', models.ForeignKey(to='radio_queue.Queue')),
                ('track', models.ForeignKey(to='radio_metadata.Track')),
            ],
            options={
                'ordering': (b'created',),
            },
            bases=(models.Model,),
        ),
    ]
