# third-party imports
from django.db import models

from radio_queue.models import Queue


class Player(models.Model):
    name = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    auth_token = models.CharField(max_length=500)
    queue = models.ForeignKey(Queue, null=True)
    active = models.BooleanField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
