# third-party imports
from django.db import models
# local imports
from radio_metadata.models import Track


PROTECTION_OPTIONS = [
    ('private', 'Private'),
    ('public', 'Public'),
]


class PlaylistManager(models.Manager):
    pass


class Playlist(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    protection = models.CharField(
        default='private', choices=PROTECTION_OPTIONS, max_length=10)
    owner = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = PlaylistManager()

    class Meta:
        unique_together = (('name', 'owner'),)
        ordering = ('name',)


class PlaylistTrackManager(models.Manager):
    def reset_track_positions(self, playlist_id):
        """Set positions of a given playlist track list."""
        records = self.filter(playlist_id=playlist_id)

        for (i, track) in enumerate(records):
            track.position = i+1
            track.save()

    def custom_create(self, track_id, playlist, owner):
        """Create playlist track."""
        track = Track.objects.get(id=track_id)
        total_playlist_records = PlaylistTrack.objects.filter(
            playlist=playlist).count()

        playlist_track = PlaylistTrack.objects.create(
            track=track,
            playlist=playlist,
            position=total_playlist_records+1,
            owner=owner
        )

        return playlist_track


class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist)
    track = models.ForeignKey(Track)
    position = models.PositiveIntegerField()
    owner = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = PlaylistTrackManager()

    class Meta:
        ordering = ('position',)
