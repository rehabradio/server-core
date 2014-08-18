import datetime
import random
# third-party imports
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import link
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


def _reset_track_positions(queue_id):
    """
    Once a record has been removed, reset the postions
    """
    records = QueueTrack.objects.filter(queue_id=queue_id)

    for (i, track) in enumerate(records):
        track.position = i+1
        track.save()


class QueueViewSet(viewsets.ModelViewSet):
    """
    CRUD API endpoints that allow managing playlists.
    """
    permission_classes = (IsStaffOrOwnerToDelete, permissions.IsAuthenticated)
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
    permission_classes = (IsStaffOrOwnerToDelete, permissions.IsAuthenticated)

    def _get_cache_key(self, queue_id):
        """Build key used for caching the playlist data
        """
        return 'queue-{0}-{1}'.format(
            queue_id, datetime.datetime.utcnow().strftime('%Y%m%d'),
        )

    def list(self, request, queue_id=None):
        """
        Returns a paginated set of tracks in a given queue
        """
        cache_key = self._get_cache_key(queue_id)
        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = QueueTrack.objects.prefetch_related(
                'track',
                'track__artists',
                'track__album',
                'track__owner',
                'owner'
            ).filter(queue_id=queue_id)
            cache.set(cache_key, queryset, 86400)
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
            queued_track = QueueTrack.objects.create(
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

        cache.delete(self._get_cache_key(kwargs['queue_id']))

        serializer = QueueTrackSerializer(queued_track)
        return Response(serializer.data)

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

        cache.delete(self._get_cache_key(kwargs['queue_id']))

        serializer = QueueTrackSerializer(queued_track)
        return Response(serializer.data)

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

        cache.delete(self._get_cache_key(kwargs['queue_id']))

        return Response({'detail': 'Queued track successfully removed'})

    @link()
    def head(self, request, *args, **kwargs):
        """
        Fetch the top track in a given queue
        """
        try:
            queued_track = QueueTrack.objects.select_related(
                'track',
                'track__album',
                'track__owner',
                'owner'
            ).get(
                queue_id=kwargs['queue_id'],
                position=1
            )
        except:
            queued_track = _add_random_track_to_queue(kwargs['queue_id'])
        seralizer = QueueTrackSerializer(queued_track)
        return Response(seralizer.data)

    @link()
    def pop(self, request, *args, **kwargs):
        """
        Remove a track from the top of a given queue
        """
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
            # reset the remaining tracks into their new positions
            _reset_track_positions(kwargs['queue_id'])
        except:
            response = {
                'detail': 'Failed to remove track from queue',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        cache.delete(self._get_cache_key(kwargs['queue_id']))

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
