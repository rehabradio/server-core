import random
# third-party imports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F

from rest_framework import generics, mixins, status, viewsets
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
from radio.permissions import IsStaffOrOwnerToDelete


def _add_random_track_to_queue(queue_id):
    """
    Grabs a random track from the queues history,
    and adds it back into the queue
    """
    # Grab the first 50 tracks with the highest number of votes
    track_ids = QueueTrackHistory.objects.filter(
        queue_id=queue_id
        ).values_list('track_id', flat=True)[:50]
    # Select a track ID at random
    track_id = random.choice(track_ids)
    # Add the track to the top of the queue
    queue_track = QueueTrack.objects.create(
        track=Track.objects.get(id=track_id),
        queue=Queue.objects.get(id=queue_id),
        position=1,
        owner_id=1
    )
    # Return the track instance
    return queue_track


class QueueViewSet(viewsets.ModelViewSet):
    """
    CRUD API endpoints that allow managing playlists.
    """
    permission_classes = (IsStaffOrOwnerToDelete, )
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Removes queue from database, and returns a detail reponse
        Must be owner or staff
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
    position -- Patch request param (int) - form
    """
    queryset = QueueTrack.objects.all()
    serializer_class = QueueTrackSerializer
    permission_classes = (IsStaffOrOwnerToDelete, )

    def list(self, request, queue_id=None):
        """
        Returns a paginated set of tracks in a given queue
        """
        queryset = QueueTrack.objects.select_related().filter(queue_id=queue_id)
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
        position = QueueTrack.objects.filter(
            queue=kwargs['queue_id']
        ).count()+1
        try:
            queue_track = QueueTrack.objects.create(
                track=Track.objects.get(id=request.DATA['track']),
                queue=Queue.objects.get(id=kwargs['queue_id']),
                position=position,
                owner_id=self.request.user.id
            )
        except:
            response = {'detail': 'Track could not be saved to queue'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            QueueTrackHistory.objects.create(
                track=Track.objects.get(id=request.DATA['track']),
                queue=Queue.objects.get(id=kwargs['queue_id']),
                owner_id=self.request.user.id
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

        new_playlist = QueueTrack.objects.filter(
            id=queued_track.id
        ).values()[0]
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


class QueueTrackHead(generics.GenericAPIView):
    """
    Fetch the top track in a given queue
    """

    serializer_class = QueueTrackSerializer

    def get(self, request, *args, **kwargs):
        try:
            queued_track = QueueTrack.objects.get(
                queue_id=kwargs['queue_id'],
                position=1
            )
        except:
            queued_track = _add_random_track_to_queue(kwargs['queue_id'])
        seralizer = QueueTrackSerializer(queued_track)
        return Response(seralizer.data)


class QueueTrackPop(mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Remove a track from the top of a given queue
    """

    serializer_class = QueueTrackSerializer

    def delete(self, request, *args, **kwargs):
        try:
            queued_track = QueueTrack.objects.get(
                queue_id=kwargs['queue_id'],
                position=1
            )
        except:
            response = {'detail': 'Queued track not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        try:
            track = queued_track.track
            track.play_count = F('play_count') + 1
            track.save()

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
