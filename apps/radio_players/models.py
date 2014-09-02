# std-lib imports
import uuid

# third-party imports
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from radio_queue.models import Queue


class Player(models.Model):
    name = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    token = models.CharField(max_length=500)
    queue = models.ForeignKey(Queue, null=True)
    active = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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
        """Create user/profile for new records.

        Finally create a unique token for the record (mopidy auth token).
        """

        if self._state.adding:

            token = uuid.uuid4()

            user = User.objects.create(
                username=self.name,
                password=token,
                is_staff=True,
            )

            self.owner = user
            self.token = token

        super(Player, self).save()
