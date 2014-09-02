# -*- coding: utf-8 -*-
# third-party imports
from django.core.cache import cache
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete

# local imports
from radio.utils.cache import build_key


class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.URLField(null=True)


def create_user_profile(sender, instance, created, **kwargs):
    cache_key = build_key('users-queryset')
    cache.delete(cache_key)

    if created:
        Profile.objects.create(user=instance)


def clear_cache(sender, **kwargs):
    cache_key = build_key('users-queryset')
    cache.delete(cache_key)

post_save.connect(create_user_profile, sender=User)
post_delete.connect(clear_cache, sender=User)
