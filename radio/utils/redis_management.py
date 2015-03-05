# -*- coding: utf-8 -*-
"""User related views
"""

# stdlib imports
import os
import json

# third-party imports
import redis


REDIS_URL = os.environ.get('REDIS_LOCATION').split(':')
REDIS_CLIENT = redis.StrictRedis(
    host=REDIS_URL[0],
    port=REDIS_URL[1],
    db=REDIS_URL[2]
)


def send_notification(channel, data):
    REDIS_CLIENT.publish(
        channel,
        json.dumps(data)
    )
