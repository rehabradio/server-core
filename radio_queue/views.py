# third-party imports
from rest_framework import status, viewsets
from rest_framework.response import Response

# local imports
from .models import Queue, QueueTrack, QueueTrackHistory
from radio_metadata.models import Track

from .serializers import QueueSerializer, QueueTrackSerializer, QueueTrackHistorySerializer


class QueueViewSet(viewsets.ModelViewSet):
    """
    CRUD API endpoints that allow managing playlists.
    """
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer

    def pre_save(self, obj):
        """
        Set user id, for each record saved/updated
        """
        obj.owner = self.request.user


class QueueTrackViewSet(viewsets.ModelViewSet):
    """
    CRUD API endpoints that allow managing playlists.
    """
    queryset = QueueTrack.objects.all()
    serializer_class = QueueTrackSerializer

    def create(self, request, *args, **kwargs):
        """
        Uses a track id to add a track to the queue
        """
        try:
            queue_track = QueueTrack.objects.create(
                track=Track.objects.get(id=request.DATA['track']),
                position=request.DATA['position'],
                owner=self.request.user
            )
        except:
            response = {'detail': 'Track could not be saved to queue'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            QueueTrackHistory.objects.create(
                track=Track.objects.get(id=request.DATA['track']),
                queue=Queue.objects.get(id=kwargs['queue_id']),
                owner=self.request.user
            )
        except:
            response = {'detail': 'Track could not be saved to queue history'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        new_playlist = QueueTrack.objects.filter(id=queue_track.id).values()[0]
        return Response(new_playlist)

    def pre_save(self, obj):
        """
        Set user id, for each record saved/updated
        """
        obj.owner = self.request.user


class QueueTrackHistoryViewSet(viewsets.ModelViewSet):
    """
    CRUD API endpoints that allow managing playlists.
    """
    queryset = QueueTrackHistory.objects.all()
    serializer_class = QueueTrackHistorySerializer

    def pre_save(self, obj):
        """
        Set user id, for each record saved/updated
        """
        obj.owner = self.request.user
