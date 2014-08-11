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


class PlaylistTrack(models.Model):
    # playlist to which this track has been added
    playlist = models.ForeignKey(Playlist)
    # track which has been added to this playlist
    track = models.ForeignKey(Track)
    # Ordering of the tracks
    position = models.PositiveIntegerField()
    owner = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('position',)
        unique_together = (('playlist', 'track'),)
