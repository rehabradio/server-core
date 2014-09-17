# std-lib imports
import uuid

# third-party imports
from django.contrib.auth.models import User, UserManager
from django.core.exceptions import ValidationError
from django.db import models

from radio_queue.models import Queue


class Player(User):
    name = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    token = models.CharField(max_length=500)
    queue = models.ForeignKey(Queue, null=True)
    active = models.BooleanField(default=False)

    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    def __unicode__(self):
        return u'%s - %s' % (self.location, self.name)

    def clean(self):
        """Ensures that only one player is active on a given queue."""
        active_player = Player.objects.filter(
            queue=self.queue, active=True).exclude(id=self.id)

        if self.active and active_player:
            raise ValidationError(
                "A player is already active on the selected queue")

    def save(self, *args, **kwargs):
        """Create a unique token for the record (mopidy auth token).
        """
        if self._state.adding:
            self.username = '{0} (Player)'.format(self.name)
            self.token = uuid.uuid4()

            super(Player, self).save()
