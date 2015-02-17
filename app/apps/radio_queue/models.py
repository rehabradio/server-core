# third-party imports
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save

# local imports
from radio_metadata.models import Track
from radio.utils.cache import build_key


class Queue(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    owner = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class QueueTrackManager(models.Manager):

    def reset_track_positions(self, queue_id):
        """Set positions of a given queue track list."""
        from .notifications import update_notification

        records = self.filter(queue_id=queue_id)

        # Disconnect the signal while updating the playlist track position
        post_save.disconnect(update_notification, sender=QueueTrack)

        for (i, track) in enumerate(records):
            track.position = i+1
            track.save()

        # Re-connect the signal after all track positions are updated
        post_save.connect(update_notification, sender=QueueTrack)

    def custom_create(self, track_id, queue_id, owner, record=True):
        """Create queue track."""
        track = Track.objects.get(id=track_id)
        queue = Queue.objects.get(id=queue_id)
        total_queue_records = self.filter(queue=queue).count()

        queue_track = self.create(
            track=track, queue=queue,
            position=total_queue_records+1, owner=owner)

        if record:
            QueueTrackHistory.objects.create(
                track=track, queue=queue, owner=owner)
            # Delete the historic track list,
            # if a track is manually added to queue
            cache.delete(build_key('queue-head-history', queue_id))

        return queue_track


class QueueTrack(models.Model):
    track = models.ForeignKey(Track)
    queue = models.ForeignKey(Queue)
    position = models.PositiveIntegerField()
    state = models.CharField(max_length=500, null=True)
    time_position = models.IntegerField(null=True)
    owner = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = QueueTrackManager()

    class Meta:
        ordering = ('position',)


class QueueTrackHistory(models.Model):
    track = models.ForeignKey(Track)
    queue = models.ForeignKey(Queue)
    owner = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
