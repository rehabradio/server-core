# third-party imports
from django.contrib.auth.models import User, UserManager
from django.core.cache import cache
from django.db import models

# local imports
from radio_queue.models import Queue
from radio.utils.cache import build_key


class Player(User):
    name = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    token = models.CharField(max_length=500)
    queue = models.ForeignKey(Queue, null=True)
    active = models.BooleanField(default=False)
    owner = models.CharField(max_length=500, default='')

    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    def __unicode__(self):
        return u'%s - %s' % (self.location, self.name)

    class Meta:
        verbose_name = "Player"

    def save(self, *args, **kwargs):
        """Set some default values.
        """
        # If no other tracks are active on the queue, then set active to true
        queryset = Player.objects.filter(queue=self.queue, active=True)
        if not queryset.count():
            self.active = True
        elif queryset.exclude(id=self.id).count():
            self.active = False

        super(Player, self).save(args, kwargs)

        cache.set(build_key('player', self.id), self)

        return self
