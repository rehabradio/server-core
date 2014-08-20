# -*- coding: utf-8 -*-
"""Playlist related views
"""
# stdlib imports
import datetime
# third-party imports
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import permissions, viewsets
from rest_framework.response import Response
# local imports
from .models import Playlist, PlaylistTrack
from .serializers import (
    PlaylistSerializer,
    PaginatedPlaylistSerializer,
    PlaylistTrackSerializer,
    PaginatedPlaylistTrackSerializer
)
from radio.exceptions import (
    RecordDeleteFailed,
    RecordNotFound,
    RecordNotSaved,
)
from radio.permissions import (
    IsOwnerOrReadOnly,
    IsOwnerOrPlaylistOwnerElseReadOnly
)
from radio_metadata.models import Track


def _reset_track_positions(playlist_id):
    """Set positions of a given playlist track list."""
    records = PlaylistTrack.objects.filter(playlist_id=playlist_id)

    for (i, track) in enumerate(records):
        track.position = i+1
        track.save()


class PlaylistViewSet(viewsets.ModelViewSet):
    """CRUD API endpoints that allow managing playlists.
    For update and delete functions, user must be owner
    """
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated)
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def _get_cache_key(self):
        """Build key used for caching the playlist data."""
        return 'playlists-{0}'.format(
            datetime.datetime.utcnow().strftime('%Y%m%d'),
        )

    def list(self, request):
        """Return a paginated list of playlist json objects."""
        cache_key = self._get_cache_key()
        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = Playlist.objects.prefetch_related(
                'owner'
            ).all()
            cache.set(cache_key, queryset, 86400)

        paginator = Paginator(queryset, 20)

        page = request.QUERY_PARAMS.get('page')
        try:
            playlists = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            playlists = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            playlists = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        serializer = PaginatedPlaylistSerializer(
            playlists, context=serializer_context
        )
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Removes playlist and its associated playlist tracks from database.
        Returns a detail reponse.
        """
        try:
            playlist = Playlist.objects.get(id=kwargs['pk'])
        except:
            raise RecordNotFound

        try:
            playlist.delete()
        except:
            raise RecordDeleteFailed

        cache.delete(self._get_cache_key())

        return Response({'detail': 'playlist successfully removed'})

    def pre_save(self, obj):
        """Set the record owner as the current logged in user,
        when creating/updating a record.

        Remove the cached track list after a database record is updated.
        """
        obj.owner = self.request.user
        cache.delete(self._get_cache_key())


class PlaylistTrackViewSet(viewsets.ModelViewSet):
    """CRUD API endpoints that allow managing playlist tracks.
    For update and delete functions, user must be owner of track or playlist

    position -- Patch request param (int) - form
    """
    permission_classes = (
        IsOwnerOrPlaylistOwnerElseReadOnly,
        permissions.IsAuthenticated
    )
    queryset = PlaylistTrack.objects.all()
    serializer_class = PlaylistTrackSerializer

    def _get_cache_key(self, playlist_id):
        """Build key used for caching the playlist data."""
        return 'playlisttracks-{0}-{1}'.format(
            playlist_id, datetime.datetime.utcnow().strftime('%Y%m%d'),
        )

    def list(self, request, playlist_id=None):
        """Return a paginated list of playlist track json objects."""
        cache_key = self._get_cache_key(playlist_id)
        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = PlaylistTrack.objects.prefetch_related(
                'track',
                'track__artists',
                'track__album',
                'track__owner',
                'owner'
            ).filter(playlist_id=playlist_id)
            cache.set(cache_key, queryset, 86400)

        paginator = Paginator(queryset, 20)

        page = request.QUERY_PARAMS.get('page')
        try:
            playlist_tracks = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            playlist_tracks = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            playlist_tracks = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        serializer = PaginatedPlaylistTrackSerializer(
            playlist_tracks, context=serializer_context
        )
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Add a track to the database.
        params - track

        Returns a the newly created track as a json object
        """
        track_id = request.POST['track']
        playlist_id = kwargs['playlist_id']
        total_playlist_records = PlaylistTrack.objects.filter(
            playlist=kwargs['playlist_id']
        ).count()

        try:
            playlist_track = PlaylistTrack.objects.create(
                track=Track.objects.get(id=track_id),
                playlist=Playlist.objects.get(id=playlist_id),
                position=total_playlist_records+1,
                owner=self.request.user
            )
        except:
            raise RecordNotSaved

        cache.delete(self._get_cache_key(playlist_id))

        serializer = PlaylistTrackSerializer(playlist_track)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Update a playlist track position.
        params - position

        Returns a the updated track as a json object
        """
        try:
            playlist_track = PlaylistTrack.objects.get(id=kwargs['pk'])
        except:
            raise RecordNotFound
        try:
            playlist_track.position = request.DATA['position']
            playlist_track.save()
        except:
            raise RecordNotSaved

        cache.delete(self._get_cache_key(playlist_track.playlist.id))

        serializer = PlaylistTrackSerializer(playlist_track)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Removes playlist track from database and resests the
        remaining track positions.

        Returns a detail reponse.
        """
        try:
            playlist_track = PlaylistTrack.objects.get(id=kwargs['pk'])
        except:
            raise RecordNotFound
        try:
            playlist_id = playlist_track.playlist.id
            playlist_track.delete()
            _reset_track_positions(playlist_id)
        except:
            raise RecordDeleteFailed

        cache.delete(self._get_cache_key(playlist_id))

        return Response({'detail': 'Track removed from playlist'})
