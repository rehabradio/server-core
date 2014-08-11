# third-party imports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import status, viewsets
from rest_framework.response import Response

# local imports
from .models import Queue, QueueTrack, QueueTrackHistory
from radio_metadata.models import Track

from .serializers import (
    QueueSerializer,
    QueueTrackSerializer,
    PaginatedQueueTrackSerializer,
    QueueTrackHistorySerializer,
    PaginatedQueueTrackHistorySerializer
)


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

    def list(self, request, queue_id=None):
        """
        Returns a paginated set of tracks in a given queue
        """
        queryset = self.queryset.filter(queue_id=queue_id)
        paginator = Paginator(queryset, 20)

        page = request.QUERY_PARAMS.get('page')
        try:
            queued_tracks = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queued_tracks = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            queued_tracks = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        serializer = PaginatedQueueTrackSerializer(
            queued_tracks, context=serializer_context
        )
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Uses a track id to add a track to the end of a queue
        """
        position = QueueTrack.objects.filter(queue=kwargs['queue_id']).count()+1
        try:
            queue_track = QueueTrack.objects.create(
                track=Track.objects.get(id=request.DATA['track']),
                queue=Queue.objects.get(id=kwargs['queue_id']),
                position=position,
                owner_id=1
            )
        except:
            response = {'detail': 'Track could not be saved to queue'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            QueueTrackHistory.objects.create(
                track=Track.objects.get(id=request.DATA['track']),
                queue=Queue.objects.get(id=kwargs['queue_id']),
                owner_id=1
            )
        except:
            response = {'detail': 'Track could not be saved to queue history'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        new_playlist = QueueTrack.objects.filter(id=queue_track.id).values()[0]
        return Response(new_playlist)

    def partial_update(self, request, *args, **kwargs):
        """
        Update a queued track's position
        """
        try:
            queued_track = QueueTrack.objects.get(id=kwargs['pk'])
            queued_track.position = request.DATA['position']
            queued_track.save()
        except:
            response = {'detail': 'Queued track could not be updated'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        new_playlist = QueueTrack.objects.filter(id=queued_track.id).values()[0]
        return Response(new_playlist)

    def destroy(self, request, *args, **kwargs):
        """
        Removes queue from database, and returns a detail reponse
        """
        try:
            queued_track = QueueTrack.objects.get(id=kwargs['pk'])
        except:
            response = {'detail': 'Queued track not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        try:
            queued_track.delete()
        except:
            response = {
                'detail': 'Failed to remove track from queue',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Queued track successfully removed'})


class QueueTrackHistoryViewSet(viewsets.ModelViewSet):
    """
    CRUD API endpoints that allow managing playlists.
    """
    queryset = QueueTrackHistory.objects.all()
    serializer_class = QueueTrackHistorySerializer

    def list(self, request, queue_id=None):
        """
        Returns a paginated set of track history records for a given queue
        """
        queryset = self.queryset.filter(queue_id=queue_id)
        paginator = Paginator(queryset, 20)

        page = request.QUERY_PARAMS.get('page')
        try:
            queued_tracks = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queued_tracks = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            queued_tracks = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        serializer = PaginatedQueueTrackHistorySerializer(
            queued_tracks, context=serializer_context
        )
        return Response(serializer.data)
