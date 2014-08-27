# third-party imports
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
# local imports
from .models import Player
from .serializers import PlayerSerializer


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
        try:
            record = Player.objects.get(id=int(kwargs['pk']))
        except:
            record = Player.objects.get(token=kwargs['pk'])

        serializer = self.serializer_class(record)
        return Response(serializer.data)
