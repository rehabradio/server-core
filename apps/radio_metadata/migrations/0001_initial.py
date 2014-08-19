# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_type', models.CharField(max_length=10, choices=[(b'spotify', b'Spotify'), (b'soundcloud', b'Soundcloud')])),
                ('source_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=500)),
                ('image', models.URLField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='album',
            unique_together=set([(b'source_type', b'source_id')]),
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_type', models.CharField(max_length=10, choices=[(b'spotify', b'Spotify'), (b'soundcloud', b'Soundcloud')])),
                ('source_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='artist',
            unique_together=set([(b'source_type', b'source_id')]),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_type', models.CharField(max_length=10, choices=[(b'spotify', b'Spotify'), (b'soundcloud', b'Soundcloud')])),
                ('source_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=500)),
                ('duration_ms', models.IntegerField()),
                ('preview_url', models.URLField()),
                ('track_number', models.IntegerField()),
                ('play_count', models.IntegerField(default=0)),
                ('vote_count', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('album', models.ForeignKey(to='radio_metadata.Album', null=True)),
                ('artists', models.ManyToManyField(to='radio_metadata.Artist')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='track',
            unique_together=set([(b'source_type', b'source_id')]),
        ),
    ]
