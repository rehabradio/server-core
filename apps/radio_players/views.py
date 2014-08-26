import uuid
# third-party imports
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
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
    permissions = (IsAdminUser,)
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def retrieve(self, request, *args, **kwargs):
        record = Player.objects.get(token=kwargs['pk'])
        serializer = self.serializer_class(record)
        return Response(serializer.data)

    @action()
    def mopidy_event(self, request, *args, **kwargs):
        return Response(request.DATA)

    @action()
    def mopidy_status(self, request, *args, **kwargs):
        return Response(request.DATA)

    def post_save(self, player, created=False):
        """
        On creation, create a token
        """
        if created:
            token = uuid.uuid4()

            user = User.objects.create(
                username=player.name,
                password=token,
                is_staff=True,
            )

            player.owner = user
            player.token = token
            player.save()
