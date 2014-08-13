# third-party imports
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

# local imports
from .models import Player
from .serializers import PlayerSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    """
    CRUD API endpoints that allow managing connected players.
    User must be admin
    """
    permission_classes = (IsAdminUser,)
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
