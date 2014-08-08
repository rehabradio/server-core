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

    def destroy(self, request, *args, **kwargs):
        """
        Removes queue from database, and returns a detail reponse
        """
        try:
            queue = Queue.objects.get(id=kwargs['pk'])
        except:
            response = {'detail': 'Queue not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        try:
            queue.delete()
        except:
            response = {
                'detail': 'Failed to remove queue',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Queue successfully removed'})

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
        Uses a track id to add a track to the end of a queue
        """
        position = QueueTrack.objects.filter(queue=kwargs['queue_id'])+1
        try:
            queue_track = QueueTrack.objects.create(
                track=Track.objects.get(id=request.DATA['track']),
                position=position,
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
