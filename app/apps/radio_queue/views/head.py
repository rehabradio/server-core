# -*- coding: utf-8 -*-
"""Queue head track related views
"""
# stdlib imports
import json
import random

# third-party imports
from django.core.cache import cache
from django.db.models import F
from rest_framework import viewsets
from rest_framework.response import Response

# local imports
from ..models import QueueTrack
from ..models import QueueTrackHistory
from ..serializers import QueueTrackSerializer
from ..serializers import QueueTrackHistorySerializer
from radio.exceptions import RecordDeleteFailed
from radio.exceptions import RecordNotFound
from radio.exceptions import RecordNotSaved
from radio.exceptions import QueueEmpty
from radio.utils.cache import build_key
from radio_metadata.views.tracks import get_associated_track


class QueueHeadViewSet(viewsets.ModelViewSet):
    """Mopidy client endpoints.
    User must be staff to delete.
    """
    queryset = QueueTrack.objects.all()
    serializer_class = QueueTrackSerializer

    def _cache_key(self, queue_id):
        """Build key used for caching the queue tracks data."""
        return build_key('queue-tracks-queryset', queue_id)

    def _history_cache_key(self, queue_id):
        """Build key used for caching the playlist tracks data."""
        return build_key('queue-head-history', queue_id)

    def retrieve(self, request, queue_id, *args, **kwargs):
        """Fetch the top track in a given queue."""
        queued_tracks = QueueTrack.objects.filter(queue_id=queue_id)
        if len(queued_tracks):
            queued_track = queued_tracks[0]
        else:
            try:
                queued_track = self._queue_radio(queue_id)
            except:
                raise QueueEmpty

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
        queued_tracks = QueueTrack.objects.filter(queue_id=queue_id)
        if len(queued_tracks):
            queued_track = queued_tracks[0]
        else:
            raise RecordNotFound

        try:
            cache.delete(self._cache_key(queue_id))
            track = queued_track.track
            track.play_count = F('play_count') + 1
            track.save()

            queued_track.delete()
        except:
            raise RecordDeleteFailed

        # reset the remaining tracks into their new positions
        QueueTrack.objects.reset_track_positions(queue_id)

        return Response({'detail': 'Track successfully removed from queue.'})

    def _queue_radio(self, queue_id):
        """Add an associated track to a given queue,
        using the queues track history.

        Uses caching to create a tracklist of tracks,
        to use as a base to find new songs.

        Caching is reset when a track is manually added to the queue.
        """
        # Tracklist to be used to find next track
        historic_tracks = cache.get(self._history_cache_key(queue_id))

        # Build tracklist from queue history
        if historic_tracks is None:
            historic_tracks = []
            queryset = QueueTrackHistory.objects.filter(
                queue_id=queue_id).order_by().distinct('track_id')
            for track in queryset:
                serializer = QueueTrackHistorySerializer(track)
                historic_tracks.append(serializer.data['track'])

        # Pick a track from the tracklist at random,
        # and remove it from the tracklist
        track = random.choice(historic_tracks)
        historic_tracks.remove(track)

        # Use the tracks main artist to fetch new track
        source_id = track['source_id']
        if track['source_type'] == 'spotify':
            source_id = track['artists'][0]['source_id']

        track = get_associated_track(
            source_id, track['source_type'], self.request.user)

        # Update the tracklist with the newly fetched track
        historic_tracks.append(track)
        cache.set(self._history_cache_key(queue_id), historic_tracks, 86400)

        # Add the new track to the queue
        queue_track = QueueTrack.objects.custom_create(
            track['id'], queue_id, self.request.user, record=False)

        return queue_track
