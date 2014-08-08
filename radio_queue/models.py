from django.db import models

# local imports
from radio_metadata.models import Track


class Queue(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    owner = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class QueueTrack(models.Model):
    track = models.ForeignKey(Track)
    position = models.PositiveIntegerField(null=True)
    owner = models.ForeignKey('auth.User', null=True)

    class Meta:
        ordering = ('position',)


class QueueTrackHistory(models.Model):
    queue = models.ForeignKey(Queue)
    track = models.ForeignKey(Track)
    owner = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
