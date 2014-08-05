from django.db import models

# local imports
from radio_metadata.models import Track


class QueuedTrack(models.Model):
    # Track
    track = models.ForeignKey(Track)
    # Timestamp of when the track was first selected
    # Used to sync devices
    started = models.DateTimeField(null=True)
    # Playing order [Position 1 is the active track]
    position = models.PositiveIntegerField(null=True)
    alive = models.BooleanField(default=True)
    owner = models.ForeignKey('auth.User', null=True)

    class Meta:
        ordering = ('position',)


class QueuedTrackHistory(models.Model):
    track = models.ForeignKey(Track)
    owner = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)


class QueuedTrackVote(models.Model):
    # Queued Track upon which this vote has been made
    queued_track = models.ForeignKey(QueuedTrack)
    # value of the vote that has been made (upvote/downvote)
    value = models.IntegerField(
        choices=[(x, x) for x in range(-1, 2)],
        default=0
    )
    owner = models.ForeignKey('auth.User')
