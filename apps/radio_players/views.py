# third-party imports
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
# local imports
from .models import Player
from .serializers import PlayerSerializer
from radio.exceptions import RecordNotFound


class PlayerViewSet(viewsets.ModelViewSet):
    """
    CRUD API endpoints that allow managing connected players.
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
        except:
            player_token = kwargs['pk']

        try:
            if player_id:
                record = Player.objects.get(id=player_id)
            else:
                record = Player.objects.get(token=player_token)
        except:
            raise RecordNotFound

        serializer = self.serializer_class(record)
        return Response(serializer.data)
