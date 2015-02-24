# third-party imports
from rest_framework import viewsets
from rest_framework.response import Response

# local imports
from .models import Player
from .serializers import PlayerSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    """List and retrieve endpoints for the players.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def retrieve(self, request, pk=None, token=None, *args, **kwargs):
        """Fetch the top track in a given queue."""
        if token:
            player = Player.objects.get(token=token)
        else:
            player = Player.objects.get(pk=pk)

        seralizer = PlayerSerializer(player)

        return Response(seralizer.data)
