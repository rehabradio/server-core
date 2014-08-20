# third-party imports
from django.db import models
# local imports
from radio_metadata.models import Track


class Playlist(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    owner = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('name', 'owner'),)
        ordering = ('name',)


class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist)
    track = models.ForeignKey(Track)
    position = models.PositiveIntegerField()
    owner = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('position',)