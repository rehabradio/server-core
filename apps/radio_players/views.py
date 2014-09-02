# third-party imports
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

# local imports
from .models import Player
from .serializers import PlayerSerializer
from radio.exceptions import RecordNotFound
from radio.utils.cache import build_key


class PlayerViewSet(viewsets.ModelViewSet):
    """List and retrieve endpoints for the players.
    User must be admin.
    """
    permissions = (IsAdminUser,)
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def retrieve(self, request, *args, **kwargs):
        """Fetch record by token or id."""
        player_id = None
        player_token = None

        try:
            player_id = int(kwargs['pk'])
            cache_key = build_key('player-details', player_id)
        except:
            player_token = kwargs['pk']
            cache_key = build_key('player-details', player_token)

        response = cache.get(cache_key)
        if response:
            return Response(response)

        try:
            if player_id:
                record = Player.objects.get(id=player_id)
            else:
                record = Player.objects.get(token=player_token)
        except:
            raise RecordNotFound

        serializer = PlayerSerializer(record)
        cache.set(cache_key, serializer.data, 86400)

        return Response(serializer.data)

    def post_save(self, obj):
        """Remove the cached player each time a record is updated."""
        id_cache_key = build_key('player-details', obj.id)
        token_cache_key = build_key('player-details', obj.token)
        cache.delete(id_cache_key)
        cache.delete(token_cache_key)

    def post_delete(self, obj):
        """Remove the cached player each time a record is delete."""
        id_cache_key = build_key('player-details', obj.id)
        token_cache_key = build_key('player-details', obj.token)
        cache.delete(id_cache_key)
        cache.delete(token_cache_key)
