# std-lib imports
import datetime

# thrid party imports
from django.core.cache import cache
from rest_framework import authentication
from rest_framework import exceptions

# local imports
from radio_players.models import Player


class PlayerTokenAuthBackend(authentication.BaseAuthentication):
    """
    Validate a player based on the token provided in the request header
    """
    def authenticate(self, request):
        # Retrieve the access token from the request header
        access_token = request.META.get('HTTP_X_PLAYER_AUTH_TOKEN')

        if access_token:
            cache_key = 'playertoken-{0}-{1}'.format(
                access_token, datetime.datetime.utcnow().strftime('%Y%m%d'),
            )
            player = cache.get(cache_key)

            if player is None:
                try:
                    player = Player.objects.get(token=access_token)
                    cache.set(cache_key, player, 3600)
                except:
                    raise exceptions.AuthenticationFailed()

            return (player, None)
        return None
