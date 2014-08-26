# third-party imports
from django.db import models

from radio_queue.models import Queue


class Player(models.Model):
    name = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    token = models.CharField(max_length=500)
    queue = models.ForeignKey(Queue, null=True)
    active = models.BooleanField(default=0)
    owner = models.ForeignKey('auth.User', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('queue', 'active'),)
