# third-party imports
from django.db import models
# local imports
from radio_metadata.models import Track


class Queue(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    owner = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)


class QueueTrack(models.Model):
    track = models.ForeignKey(Track)
    queue = models.ForeignKey(Queue)
    position = models.PositiveIntegerField()
    state = models.CharField(max_length=500, null=True)
    time_position = models.IntegerField(null=True)
    owner = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('position',)


class QueueTrackHistory(models.Model):
    track = models.ForeignKey(Track)
    queue = models.ForeignKey(Queue)
    owner = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
