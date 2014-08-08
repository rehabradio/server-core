# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.models import User
from django.conf import settings


def update_owner(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Track = apps.get_model("radio_metadata", "Track")
    user = User.objects.get(id=1)
    for track in Track.objects.all():
        track.owner_id = user.id
        track.save()


class Migration(migrations.Migration):

    dependencies = [
        ('radio_metadata', '0003_remove_track_vote_count'),
    ]

    operations = [
        migrations.RunPython(update_owner),
        migrations.AlterField(
            model_name='track',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
