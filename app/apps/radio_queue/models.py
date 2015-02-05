# third-party imports
from django.core.cache import cache
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete

# local imports
from radio_metadata.models import Track
from radio.utils.cache import build_key
from radio.utils.redis_management import send_notification


def _notification(channel, status, queue_id, is_track):
    data = {
        'status': status,
        'data': {
            'queue_id': queue_id,
            'is_track': is_track
        }
    }

    send_notification(channel, data)


def update_notification(sender, instance, created, **kwargs):
    is_track = False
    status = ('updated', 'created')[int(bool(created))]

    # Check if it is a track or queue update
    if hasattr(instance, 'queue'):
        # Check to ensure it is not reporting on the head track
        if instance.position == 1:
            return

        queue_id = instance.queue.id
        is_track = True
    else:
        queue_id = instance.id

    return _notification('queues', status, queue_id, is_track)


def delete_notification(sender, **kwargs):
    is_track = False
    # Check if it is a track or queue update
    if hasattr(kwargs['instance'], 'queue'):
        queue_id = kwargs['instance'].queue.id
        is_track = True
    else:
        queue_id = kwargs['instance'].id

    return _notification('queues', 'deleted', queue_id, is_track)


def head_notification(sender, instance, **kwargs):
    if hasattr(instance, 'id'):
        QueueTrack.objects.filter(queue_id=instance.queue.id, position=1)
        try:
            org_head = QueueTrack.objects.get(queue_id=instance.queue.id, position=1)
        except:
            return
            # return _notification('queue-heads', 'removed', instance.queue.id, True)

        if org_head is not None:
            # Check to see if new track is at the queue head
            if org_head.id == instance.id:
                org_track = QueueTrack.objects.get(id=instance.id)

                # Check to see if the playing state has changed
                if org_track.state != instance.state:
                    return _notification('queue-heads', 'updated', instance.queue.id, True)


class Queue(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    owner = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class QueueTrackManager(models.Manager):

    def _history_cache_key(self, queue_id):
        """Build key used for caching the queue tracks data."""
        return build_key('queue-head-history', queue_id)

    def reset_track_positions(self, queue_id):
        """Set positions of a given queue track list."""
        records = self.filter(queue_id=queue_id)

        for (i, track) in enumerate(records):
            # Disconnect the signal while updating the playlist track position
            post_save.disconnect(update_notification, sender=QueueTrack)

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
            cache.delete(self._history_cache_key(queue_id))

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


post_save.connect(update_notification, sender=Queue)
post_save.connect(update_notification, sender=QueueTrack)

pre_save.connect(head_notification, sender=QueueTrack)

post_delete.connect(delete_notification, sender=Queue)
post_delete.connect(delete_notification, sender=QueueTrack)
