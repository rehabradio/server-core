# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.models import User


def update_owner(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Track = apps.get_model("radio_metadata", "Track")
    for track in Track.objects.filter():
        track.owner_id = 1
        track.save()


class Migration(migrations.Migration):

    dependencies = [
        ('radio_metadata', '0004_auto_20140808_1103'),
    ]

    operations = [
        migrations.RunPython(update_owner),
    ]
