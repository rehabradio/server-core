# -*- coding: utf-8 -*-
"""Queue related views
"""
# stdlib imports
import json
import random

# third-party imports
from django.core.cache import cache
from django.db.models import F
from rest_framework import permissions, viewsets
from rest_framework.response import Response

# local imports
from .models import Queue, QueueTrack, QueueTrackHistory
from .serializers import (
    QueueSerializer, PaginatedQueueSerializer,
    QueueTrackSerializer, PaginatedQueueTrackSerializer,
    QueueTrackHistorySerializer, PaginatedQueueTrackHistorySerializer)
from radio.exceptions import RecordDeleteFailed, RecordNotFound, RecordNotSaved
from radio.permissions import IsStaffOrOwnerToDelete
from radio.utils.cache import build_key
from radio.utils.pagination import paginate_queryset
from radio_metadata.models import Track
from radio_metadata.views import get_associated_track
from radio_playlists.models import PlaylistTrack


class QueueViewSet(viewsets.ModelViewSet):
    """CRUD API endpoints that allow managing queue."""
    cache_key = build_key('queue-queryset')
    permission_classes = (IsStaffOrOwnerToDelete, permissions.IsAuthenticated)
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer

    def list(self, request):
        """Return a paginated list of queue json objects."""
        page = int(request.QUERY_PARAMS.get('page', 1))

        queryset = cache.get(self.cache_key)
        if queryset is None:
            queryset = Queue.objects.select_related('owner').all()
            cache.set(self.cache_key, queryset, 86400)

        response = paginate_queryset(
            PaginatedQueueSerializer, request, queryset, page)

        return Response(response)

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
            cache.delete(self.cache_key)
        except:
            raise RecordDeleteFailed

        return Response({'detail': 'Queue successfully removed.'})

    def pre_save(self, obj):
        """Set the record owner as the current logged in user,
        when creating/updating a record.

        Remove the cached track list after a database record is updated.
        """
        obj.owner = self.request.user
        cache.delete(self.cache_key)


class QueueTrackViewSet(viewsets.ModelViewSet):
    """CRUD API endpoints that allow managing queue tracks.
    User must be staff to delete

    position -- Patch request param (int) - form
    """
    queryset = QueueTrack.objects.all()
    serializer_class = QueueTrackSerializer
    permission_classes = (IsStaffOrOwnerToDelete, permissions.IsAuthenticated)

    def _cache_key(self, queue_id):
        """Build key used for caching the playlist tracks data."""
        return build_key('queue-tracks-queryset', queue_id)

    def list(self, request, queue_id=None):
        """Return a paginated list of queue track json objects."""
        page = int(request.QUERY_PARAMS.get('page', 1))

        queryset = cache.get(self._cache_key(queue_id))
        if queryset is None:
            queryset = QueueTrack.objects.prefetch_related(
                'track', 'track__artists', 'track__album',
                'track__owner', 'owner'
            ).filter(queue_id=queue_id)
            cache.set(self._cache_key(queue_id), queryset, 86400)

        response = paginate_queryset(
            PaginatedQueueTrackSerializer, request, queryset, page)

        return Response(response)

    def create(self, request, queue_id, *args, **kwargs):
        """Add tracks to a given queue.
        params - track or playlist

        Returns a list of the newly added queue_track objects
        """
        queued_tracks = []

        if 'playlist' in request.DATA:
            playlist_tracks = PlaylistTrack.objects.prefetch_related(
                'track', 'track__artists',
                'track__album', 'track__owner', 'owner'
            ).filter(playlist_id=request.DATA['playlist'])
            track_ids = ()
            for playlist_track in playlist_tracks:
                track_ids = track_ids + (playlist_track.track.id,)

        else:
            track_ids = (request.DATA['track'],)

        for track_id in track_ids:
            try:
                queued_track = QueueTrack.objects.custom_create(
                    track_id, queue_id, self.request.user)
                queued_tracks.append(QueueTrackSerializer(queued_track).data)
            except:
                raise RecordNotSaved

        cache.delete(self._cache_key(queue_id))
        return Response(queued_tracks)

    def partial_update(self, request, queue_id, pk, *args, **kwargs):
        """Update a queue track position.
        params - position

        Returns a the updated track as a json object
        """
        try:
            queued_track = QueueTrack.objects.get(id=pk)
        except:
            raise RecordNotFound

        try:
            queued_track.position = request.DATA['position']
            queued_track.save()
        except:
            raise RecordNotSaved

        cache.delete(self._cache_key(queue_id))

        serializer = QueueTrackSerializer(queued_track)
        return Response(serializer.data)

    def destroy(self, request, queue_id, pk, *args, **kwargs):
        """Removes queue track from database and resests the
        remaining track positions.

        Returns a detail reponse.
        """
        try:
            queued_track = QueueTrack.objects.get(id=pk)
        except:
            raise RecordNotFound

        try:
            queued_track.delete()
        except:
            raise RecordDeleteFailed

        # reset the remaining tracks into their new positions
        QueueTrack.objects.reset_track_positions(queue_id)
        cache.delete(self._cache_key(queue_id))

        return Response({'detail': 'Track successfully removed from queue.'})


class QueueHeadViewSet(viewsets.ModelViewSet):
    """Mopidy client endpoints.
    User must be staff to delete.
    """
    queryset = QueueTrack.objects.all()
    serializer_class = QueueTrackSerializer

    def _tracklist_cache_key(self, queue_id):
        """Build key used for caching the playlist tracks data."""
        return build_key('queue-tracks-queryset', queue_id)

    def _head_cache_key(self, queue_id):
        """Build key used for caching the playlist tracks data."""
        return build_key('queue-head-track', queue_id)

    def _history_cache_key(self, queue_id):
        """Build key used for caching the playlist tracks data."""
        return build_key('queue-head-history', queue_id)

    def retrieve(self, request, queue_id, *args, **kwargs):
        """Fetch the top track in a given queue."""
        try:
            queued_track = QueueTrack.objects.get(
                queue_id=queue_id, position=1)
        except:
            try:
                queued_track = self._artist_radio(queue_id)
            except:
                queued_track = self._add_random_track(queue_id)

        cache.set(self._head_cache_key(queue_id), queued_track.track, 86400)

        seralizer = QueueTrackSerializer(queued_track)
        return Response(seralizer.data)

    def partial_update(self, request, queue_id, *args, **kwargs):
        """Updates the head track of a given queue,
        based on the mopidy playback status.
        """
        post_data = json.loads(request.DATA)

        try:
            queued_track = QueueTrack.objects.get(
                queue_id=queue_id, position=1)
        except:
            raise RecordNotFound

        try:
            if 'state' in post_data:
                queued_track.state = post_data['state']
            if 'time_position' in post_data:
                queued_track.time_position = post_data['time_position']

            queued_track.save()
        except:
            raise RecordNotSaved

        serializer = QueueTrackSerializer(queued_track)
        return Response(serializer.data)

    def destroy(self, request, queue_id, *args, **kwargs):
        """Remove a track from the top of a given queue."""
        try:
            queued_track = QueueTrack.objects.get(
                queue_id=queue_id, position=1)
        except:
            raise RecordNotFound

        try:
            track = queued_track.track
            track.play_count = F('play_count') + 1
            track.save()

            queued_track.delete()
        except:
            raise RecordDeleteFailed

        # reset the remaining tracks into their new positions
        QueueTrack.objects.reset_track_positions(queue_id)
        cache.delete(self._tracklist_cache_key(queue_id))

        return Response({'detail': 'Track successfully removed from queue.'})

    def _add_random_track(self, queue_id):
        """Adds a random track from either the queue history or all tracks,
        to a given queue.

        Uses caching to list tracks and pops of each track as it is played.
        Caching is reset when a track is manually added to the queue.
        """
        previous_track = cache.get(self._head_cache_key(queue_id))
        historic_tracks = cache.get(self._history_cache_key(queue_id))

        if not historic_tracks:
            historic_tracks = list(QueueTrackHistory.objects.filter(
                queue_id=queue_id).order_by(
                ).values_list('track_id', flat=True).distinct())

            if not historic_tracks:
                historic_tracks = list(Track.objects.all().order_by(
                    'play_count').values_list('id', flat=True)[:50])

        if len(historic_tracks) > 1 and previous_track:
            if previous_track.id in historic_tracks:
                historic_tracks.remove(previous_track.id)

        # Select a track ID at random
        track_id = random.choice(historic_tracks)
        # Remove track from list and cache remaining tracks
        historic_tracks.remove(track_id)
        cache.set(self._history_cache_key(queue_id), historic_tracks, 86400)
        # Add the track to the top of the queue
        queue_track = QueueTrack.objects.custom_create(
            track_id, queue_id, self.request.user, record=False)

        return queue_track

    def _artist_radio(self, queue_id):
        artist = None
        source_type = 'spotify'
        previous_track = cache.get(self._head_cache_key(queue_id))
        if previous_track:
            if previous_track.source_type == source_type:
                artist = previous_track.track.artists[0]

        if artist is None:
            historic_tracks = QueueTrackHistory.objects.filter(
                queue_id=queue_id, track__source_type=source_type).order_by(
                '?')[0]
            previous_track = QueueTrackHistorySerializer(historic_tracks).data

            if previous_track:
                artist = previous_track['track']['artists'][0]
            else:
                raise RecordNotFound

        track = get_associated_track(artist, self.request.user)

        queue_track = QueueTrack.objects.custom_create(
            track['id'], queue_id, self.request.user, record=False)

        return queue_track


class QueueTrackHistoryViewSet(viewsets.ModelViewSet):
    """CRUD API endpoints that allow managing queue history tracks."""
    queryset = QueueTrackHistory.objects.all()
    serializer_class = QueueTrackHistorySerializer

    def list(self, request, queue_id=None):
        """Return a paginated list of historic queue track json objects."""
        page = int(request.QUERY_PARAMS.get('page', 1))

        queryset = QueueTrackHistory.objects.prefetch_related(
            'track', 'track__artists', 'track__album',
            'track__owner', 'owner'
        ).filter(queue_id=queue_id)

        response = paginate_queryset(
            PaginatedQueueTrackHistorySerializer, request, queryset, page)

        return Response(response)
