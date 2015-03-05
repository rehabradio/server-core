# -*- coding: utf-8 -*-
"""Queued tracks related views
"""
# third-party imports
from django.core.cache import cache
from rest_framework import permissions, viewsets
from rest_framework.response import Response

# local imports
from ..models import QueueTrack
from ..serializers import QueueTrackSerializer
from ..serializers import PaginatedQueueTrackSerializer
from radio.exceptions import RecordDeleteFailed
from radio.exceptions import RecordNotFound
from radio.exceptions import RecordNotSaved
from radio.permissions import IsStaffOrOwnerToDelete
from radio.utils.cache import build_key
from radio.utils.pagination import paginate_queryset
from radio_metadata.views.tracks import track_exists
from radio_playlists.models import PlaylistTrack


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

        # Ensure track exists in the database, and still exists at its source.
        for track_id in track_ids:
            # Throws an exception if track is not found,
            # or source no longer exists
            track_exists(track_id=track_id)

        # Save each track to the queue
        for track_id in track_ids:
            try:
                cache.delete(self._cache_key(queue_id))
                queued_track = QueueTrack.objects.custom_create(
                    track_id, queue_id, self.request.user)
                queued_tracks.append(QueueTrackSerializer(queued_track).data)
            except:
                raise RecordNotSaved

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
            cache.delete(self._cache_key(queue_id))
            queued_track.position = request.DATA['position']
            queued_track.save()
        except:
            raise RecordNotSaved

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
            cache.delete(self._cache_key(queue_id))
            queued_track.delete()
        except:
            raise RecordDeleteFailed

        # reset the remaining tracks into their new positions
        QueueTrack.objects.reset_track_positions(queue_id)

        return Response({'detail': 'Track successfully removed from queue.'})
