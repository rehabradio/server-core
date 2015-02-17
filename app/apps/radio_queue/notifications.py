# third-party imports
from django.db.models.signals import pre_save, post_save, post_delete

# local imports
from .models import Queue
from .models import QueueTrack
from radio.utils.redis_management import send_notification


def _notification(channel, status, queue_id, is_track):
    """Packages the message into a structured object
    to be passed to the redis server.
    """
    data = {
        'status': status,
        'data': {
            'queue_id': queue_id,
            'is_track': is_track
        }
    }

    send_notification(channel, data)


def update_notification(sender, instance, created, **kwargs):
    """Sends a message to the redis server
    each time an update is done on a model record.
    """

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
    """Sends a message to the redis server
    each time a record is removed from the database.
    """

    is_track = False
    # Check if it is a track or queue update
    if hasattr(kwargs['instance'], 'queue'):
        queue_id = kwargs['instance'].queue.id
        is_track = True
    else:
        queue_id = kwargs['instance'].id

    return _notification('queues', 'deleted', queue_id, is_track)


def head_notification(sender, instance, **kwargs):
    """Sends a message to the redis server
    each time the head track is update.
    """
    # Only run on existing records
    if hasattr(instance, 'id'):
        queued_tracks = QueueTrack.objects.filter(queue_id=instance.queue.id)

        # If there are tracks in the queue, then grab the top track
        if len(queued_tracks):
            org_head = queued_tracks[0]

            # Check to see if new track is at the queue head
            if org_head.id == instance.id:
                org_track = QueueTrack.objects.get(id=instance.id)

                # Check to see if the playing state has changed
                if org_track.state != instance.state:
                    return _notification('queue-heads', 'updated', instance.queue.id, True)


# Signal connects for each model instance
pre_save.connect(head_notification, sender=QueueTrack)

post_save.connect(update_notification, sender=Queue)
post_save.connect(update_notification, sender=QueueTrack)

post_delete.connect(delete_notification, sender=Queue)
post_delete.connect(delete_notification, sender=QueueTrack)
