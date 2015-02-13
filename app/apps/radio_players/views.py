# third-party imports
from rest_framework import viewsets
from rest_framework.response import Response

# local imports
from .models import Player
from .serializers import PlayerSerializer
from radio.exceptions import RecordNotFound
from radio.exceptions import RecordNotSaved
from radio_queue.models import Queue


class PlayerViewSet(viewsets.ModelViewSet):
    """List and retrieve endpoints for the players.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def update(self, request, pk, *args, **kwargs):
        """Allows updating selected fields of a player record.
        """

        try:
            player = Player.objects.get(id=pk)
        except:
            raise RecordNotFound

        try:
            if 'active' in request.DATA:
                player.active = request.DATA['active']
            if 'queue' in request.DATA:
                player.queue = Queue.objects.get(id=request.DATA['queue'])
            player.save()
        except:
            raise RecordNotSaved

        serializer = PlayerSerializer(player)
        return Response(serializer.data)
