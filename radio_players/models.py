# third-party imports
from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    auth_token = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
