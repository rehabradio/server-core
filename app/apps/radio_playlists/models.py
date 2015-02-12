# third-party imports
from django.db import models
from django.db.models.signals import post_save, post_delete

# local imports
from radio_metadata.models import Track
from radio.utils.redis_management import send_notification


PROTECTION_OPTIONS = [
    ('private', 'Private'),
    ('public', 'Public'),
]


def _notification(status, playlist_id, is_track):
    channel = 'playlists'
    data = {
        'status': status,
        'data': {
            'playlist_id': playlist_id,
            'is_track': is_track
        }
    }

    send_notification(channel, data)


def update_notification(sender, instance, created, **kwargs):
    is_track = False
    status = ('updated', 'created')[int(bool(created))]

    # Check if it is a track or playlist update
    if hasattr(instance, 'playlist'):
        playlist_id = instance.playlist.id
        is_track = True
    else:
        playlist_id = instance.id

    return _notification(status, playlist_id, is_track)


def delete_notification(sender, **kwargs):
    is_track = False
    # Check if it is a track or playlist update
    if hasattr(kwargs['instance'], 'playlist'):
        playlist_id = kwargs['instance'].playlist.id
        is_track = True
    else:
        playlist_id = kwargs['instance'].id

    return _notification('deleted', playlist_id, is_track)


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

        # Disconnect the signal while updating the playlist track position
        post_save.disconnect(update_notification, sender=PlaylistTrack)

        for (i, track) in enumerate(records):
            track.position = i+1
            track.save()

        # Re-connect the signal after all track positions are updated
        post_save.connect(update_notification, sender=PlaylistTrack)

    def custom_create(self, track_id, playlist, owner):
        """Create playlist track."""
        track = Track.objects.get(id=track_id)
        total_playlist_records = self.filter(
            playlist=playlist).count()

        playlist_track = self.create(
            track=track, playlist=playlist,
            position=total_playlist_records+1, owner=owner)

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


post_save.connect(update_notification, sender=Playlist)
post_save.connect(update_notification, sender=PlaylistTrack)

post_delete.connect(delete_notification, sender=Playlist)
post_delete.connect(delete_notification, sender=PlaylistTrack)
