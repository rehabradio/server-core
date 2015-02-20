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

    def get_player(self, user_id):
        c_key = build_key('player', user_id)
        player = cache.get(c_key)

        # If no player is found, trigger a model save which caches the player record
        # This ensures that players are always up to date.
        if player:
            # If player is not active, save the record, which will try to set active to true
            # if it is the only player listening on a given queue
            if player.active is False:
                player = Player.objects.get(pk=user_id).save()
        else:
            player = Player.objects.get(pk=user_id).save()

        return player

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
