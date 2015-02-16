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
from radio.exceptions import RecordNotSaved
from radio.exceptions import RecordNotFound
from radio.utils.cache import build_key
from radio_metadata.views.tracks import get_associated_track
from radio_players.models import Player


class QueueHeadViewSet(viewsets.ModelViewSet):
    """Operations for the top track of a given queue.
    Players must be "active" on a given queue, to modify the track.
    """
    queryset = QueueTrack.objects.all()
    serializer_class = QueueTrackSerializer

    def _cache_key(self, queue_id):
        """Build key used for caching the queue tracks data."""
        return build_key('queue-head-track', queue_id)

    def _history_cache_key(self, queue_id):
        """Build key used for caching the playlist tracks data."""
        return build_key('queue-head-history', queue_id)

    def _get_player(self):
        """Fetches the player data.
        This is used over `self.request.user` to allow active updates on the player.
        """
        # If player is not active, save the record, which will try to set active to true
        # if it is the only player listening on a given queue
        if self.request.user.active is False:
            Player.objects.get(pk=self.request.user).save()

        c_key = build_key('player', self.request.user.id)
        player = cache.get(c_key)
        # If no player data is found in cache, then use the current user data
        if player is None:
            player = self.request.user
            cache.set(c_key, self.request.user)

        return player

    def get_head_track(self, queue_id, is_active, random=False):
        """Look up the track at the top of a given queue.

        If queue is empty and "random" is set to True,
        will fetch a random track, based of the queues history.

        Returns serialized track or None.
        """
        head_track = cache.get(self._cache_key(queue_id))
        if head_track is None and is_active:
            queued_tracks = QueueTrack.objects.filter(queue_id=queue_id)
            # If there are tracks in the queue, then grab the top track
            if len(queued_tracks):
                head_track = queued_tracks[0]
            else:
                # Else use a randomly selected track
                head_track = self._queue_radio(queue_id)

            if head_track:
                expire_in = (head_track.track.duration_ms/1000) - 5
                cache.set(self._cache_key(queue_id), head_track, expire_in)

        return head_track

    def retrieve(self, request, queue_id=None, *args, **kwargs):
        """Fetch the top track in a given queue."""
        is_active = True

        if queue_id is None:
            player = self._get_player()
            is_active = player.active
            queue_id = player.queue.id

        head_track = self.get_head_track(queue_id, is_active, random=True)
        seralizer = QueueTrackSerializer(head_track)

        return Response(seralizer.data)

    def partial_update(self, request, queue_id=None, *args, **kwargs):
        """Updates the head track of a given queue,
        based on the mopidy playback status.
        """
        is_active = True
        post_data = json.loads(request.DATA)

        if queue_id is None:
            player = self._get_player()
            is_active = player.active
            queue_id = player.queue.id

        head_track = self.get_head_track(queue_id, is_active)

        # Ensure the post data matches the queue,
        # and user is active and allowed to update record.
        if post_data['queue_id'] == queue_id and is_active:
            try:
                if 'state' in post_data:
                    head_track.state = post_data['state']
                if 'time_position' in post_data:
                    head_track.time_position = post_data['time_position']

                # Set the cache to expire when track finishes
                time_til_end = head_track.track.duration_ms - head_track.time_position
                cache.set(self._cache_key(queue_id), head_track, (time_til_end/1000) - 4)

                head_track.save()
            except:
                raise RecordNotSaved

        serializer = QueueTrackSerializer(head_track)
        return Response(serializer.data)

    def destroy(self, request, queue_id=None, *args, **kwargs):
        """Remove a track from the top of a given queue,
        and return the next track.
        """
        is_active = True
        post_queue_id = queue_id

        if queue_id is None:
            player = self._get_player()
            is_active = player.active
            queue_id = player.queue.id
            post_data = json.loads(request.DATA)
            post_queue_id = post_data['queue_id']

        # Ensure the post data matches the queue,
        # and user is active and allowed to update record.
        if post_queue_id == queue_id and is_active:
            queue_tracks = QueueTrack.objects.filter(queue_id=queue_id)
            if len(queue_tracks):
                head_track = queue_tracks[0]
            else:
                raise RecordNotFound

            try:
                # Update the play count for the given track
                track = head_track.track
                track.play_count = F('play_count') + 1
                track.save()

                cache.delete(self._cache_key(queue_id))
                head_track.delete()
            except:
                raise RecordDeleteFailed

            # reset the remaining tracks into their new positions
            QueueTrack.objects.reset_track_positions(queue_id)

        # Call get_head_track method to reset cache
        new_head_track = self.get_head_track(queue_id, is_active, random=True)

        seralizer = QueueTrackSerializer(new_head_track)

        return Response(seralizer.data)

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

            # If there is nothing in the queues track history, then exit
            if not queryset:
                return None

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
