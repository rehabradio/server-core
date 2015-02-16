# third-party imports
from rest_framework import viewsets

# local imports
from .models import Player
from .serializers import PlayerSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    """List and retrieve endpoints for the players.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
