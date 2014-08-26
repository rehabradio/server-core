# -*- coding: utf-8 -*-
"""Queue related views
"""
# stdlib imports
import datetime
import random
# third-party imports
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F
from rest_framework import permissions, viewsets
from rest_framework.decorators import action, link
from rest_framework.response import Response
# local imports
from .models import Queue, QueueTrack, QueueTrackHistory
from .serializers import (
    QueueSerializer,
    PaginatedQueueSerializer,
    QueueTrackSerializer,
    PaginatedQueueTrackSerializer,
    QueueTrackHistorySerializer,
    PaginatedQueueTrackHistorySerializer
)
from radio.exceptions import (
    RecordDeleteFailed,
    RecordNotFound,
    RecordNotSaved,
)
from radio.permissions import IsStaffOrOwnerToDelete
from radio_metadata.models import Track


def _add_random_track_to_queue(queue_id, user_id):
    """Grabs a random track from the queues history,
    and adds it back into the queue

    returns track json object
    """
    track_ids = QueueTrackHistory.objects.filter(
        queue_id=queue_id).values_list('track_id', flat=True)[:50]
    if not track_ids:
        track_ids = Track.objects.all().order_by(
            'play_count').values_list('id', flat=True)[:50]
    # Select a track ID at random
    track_id = random.choice(track_ids)
    # Add the track to the top of the queue
    queue_track = QueueTrack.objects.create(
        track=Track.objects.get(id=track_id),
        queue=Queue.objects.get(id=queue_id),
        position=1,
        owner_id=user_id
    )
    # Return the track instance
    return queue_track


def _reset_track_positions(queue_id):
    """Set positions of a given queue track list."""
    records = QueueTrack.objects.filter(queue_id=queue_id)

    for (i, track) in enumerate(records):
        track.position = i+1
        track.save()


class QueueViewSet(viewsets.ModelViewSet):
    """CRUD API endpoints that allow managing queue."""
    permission_classes = (IsStaffOrOwnerToDelete, permissions.IsAuthenticated)
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer

    def _get_cache_key(self):
        """Build key used for caching the queue list."""
        return 'queuelist-{0}'.format(
            datetime.datetime.utcnow().strftime('%Y%m%d'),
        )

    def list(self, request, queue_id=None):
        """Return a paginated list of queue json objects."""
        cache_key = self._get_cache_key()
        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = Queue.objects.select_related(
                'owner'
            ).all()
            cache.set(cache_key, queryset, 86400)
        paginator = Paginator(queryset, 20)

        page = request.QUERY_PARAMS.get('page')
        try:
            queues = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queues = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            queues = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        serializer = PaginatedQueueSerializer(
            queues, context=serializer_context
        )
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Removes queue and its associated queue tracks from database.
        Returns a detail reponse.
        """
        try:
            queue = Queue.objects.get(id=kwargs['pk'])
        except:
            raise RecordNotFound

        try:
            queue.delete()
        except:
            raise RecordDeleteFailed

        cache.delete(self._get_cache_key())

        return Response({'detail': 'Queue successfully removed.'})

    def pre_save(self, obj):
        """Set the record owner as the current logged in user,
        when creating/updating a record.

        Remove the cached track list after a database record is updated.
        """
        obj.owner = self.request.user
        cache.delete(self._get_cache_key())


class QueueTrackViewSet(viewsets.ModelViewSet):
    """CRUD API endpoints that allow managing queue tracks.
    User must be staff to delete

    position -- Patch request param (int) - form
    """
    queryset = QueueTrack.objects.all()
    serializer_class = QueueTrackSerializer
    permission_classes = (IsStaffOrOwnerToDelete, permissions.IsAuthenticated)

    def _get_cache_key(self, queue_id):
        """Build key used for caching the queue data."""
        return 'queue-{0}-{1}'.format(
            queue_id, datetime.datetime.utcnow().strftime('%Y%m%d'),
        )

    def list(self, request, queue_id=None):
        """Return a paginated list of queue track json objects."""
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
        """Add a track to the database.
        params - track

        Returns a the newly created track as a json object
        """
        position = QueueTrack.objects.filter(
            queue=kwargs['queue_id']
        ).count()
        try:
            queued_track = QueueTrack.objects.create(
                track=Track.objects.get(id=request.DATA['track']),
                queue=Queue.objects.get(id=kwargs['queue_id']),
                position=position+1,
                owner=self.request.user
            )
            QueueTrackHistory.objects.create(
                track=Track.objects.get(id=request.DATA['track']),
                queue=Queue.objects.get(id=kwargs['queue_id']),
                owner=self.request.user
            )
        except:
            raise RecordNotSaved

        cache.delete(self._get_cache_key(kwargs['queue_id']))

        serializer = QueueTrackSerializer(queued_track)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Update a queue track position.
        params - position

        Returns a the updated track as a json object
        """
        try:
            queued_track = QueueTrack.objects.get(id=kwargs['pk'])
        except:
            raise RecordNotFound
        try:
            queued_track.position = request.DATA['position']
            queued_track.save()
        except:
            raise RecordNotSaved

        cache.delete(self._get_cache_key(kwargs['queue_id']))

        serializer = QueueTrackSerializer(queued_track)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Removes queue track from database and resests the
        remaining track positions.

        Returns a detail reponse.
        """
        try:
            queued_track = QueueTrack.objects.get(id=kwargs['pk'])
        except:
            raise RecordNotFound

        try:
            queued_track.delete()
        except:
            raise RecordDeleteFailed

        cache.delete(self._get_cache_key(kwargs['queue_id']))

        return Response({'detail': 'Track successfully removed from queue.'})

    @link()
    def head(self, request, *args, **kwargs):
        """Fetch the top track in a given queue."""
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
            queued_track = _add_random_track_to_queue(
                kwargs['queue_id'],
                request.user.id
            )
        seralizer = QueueTrackSerializer(queued_track)
        return Response(seralizer.data)

    @action()
    def pop(self, request, *args, **kwargs):
        """Remove a track from the top of a given queue."""
        try:
            queued_track = QueueTrack.objects.get(
                queue_id=kwargs['queue_id'],
                position=1
            )
        except:
            raise RecordNotFound

        try:
            track = queued_track.track
            track.play_count = F('play_count') + 1
            track.save()

            queued_track.delete()
            # reset the remaining tracks into their new positions
            _reset_track_positions(kwargs['queue_id'])
        except:
            raise RecordDeleteFailed

        cache.delete(self._get_cache_key(kwargs['queue_id']))

        return Response({'detail': 'Track successfully removed from queue.'})


class QueueTrackHistoryViewSet(viewsets.ModelViewSet):
    """CRUD API endpoints that allow managing queue history tracks."""
    queryset = QueueTrackHistory.objects.all()
    serializer_class = QueueTrackHistorySerializer

    def list(self, request, queue_id=None):
        """Return a paginated list of queue history track json objects."""
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
