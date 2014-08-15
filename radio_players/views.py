import uuid
# third-party imports
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

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

    def post_save(self, player, created=False):
        """
        On creation, create a token
        """
        if created:
            player.token = uuid.uuid4()
            player.save()
