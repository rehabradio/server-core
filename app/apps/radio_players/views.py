# third-party imports
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

# local imports
from .models import Player
from .serializers import PlayerSerializer
from radio.exceptions import UserIsNotPlayer


class PlayerViewSet(viewsets.ModelViewSet):
    """List and retrieve endpoints for the players.
    User must be admin.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    @detail_route(methods=['get'])
    def profile(self, request):
        try:
            serializer = PlayerSerializer(request.user)
            return Response(serializer.data)
        except:
            raise UserIsNotPlayer
