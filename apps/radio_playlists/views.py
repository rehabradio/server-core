# -*- coding: utf-8 -*-
"""Playlist related views
"""
# third-party imports
from django.core.cache import cache
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

# local imports
from .models import Playlist, PlaylistTrack
from .serializers import (
    PlaylistSerializer, PaginatedPlaylistSerializer,
    PlaylistTrackSerializer, PaginatedPlaylistTrackSerializer)
from radio.exceptions import RecordDeleteFailed, RecordNotFound, RecordNotSaved
from radio.permissions import IsOwnerOrReadOnly
from radio.utils.cache import build_key
from radio.utils.pagination import paginate_queryset


class PlaylistViewSet(viewsets.ModelViewSet):
    """CRUD API endpoints that allow managing playlists.
    For update and delete functions, user must be owner.
    """

    cache_key = build_key('playlists-queryset')
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated)
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def list(self, request):
        """Return a paginated list of playlist json objects."""
        page = int(request.QUERY_PARAMS.get('page', 1))

        queryset = cache.get(self.cache_key)
        if queryset is None:
            queryset = Playlist.objects.select_related('owner').all()
            cache.set(self.cache_key, queryset, 86400)

        response = paginate_queryset(
            PaginatedPlaylistSerializer, request, queryset, page)

        return Response(response)

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
            cache.delete(self.cache_key)
        except:
            raise RecordDeleteFailed

        return Response({'detail': 'playlist successfully removed'})

    def pre_save(self, obj):
        """Set the record owner as the current logged in user,
        when creating/updating a record.

        Remove the cached track list after a database record is updated.
        """
        obj.owner = self.request.user
        cache.delete(self.cache_key)


class PlaylistTrackViewSet(viewsets.ModelViewSet):
    """CRUD API endpoints that allow managing playlist tracks.
    For update and delete functions, user must be owner of track or playlist

    position -- Patch request param (int) - form
    """
    queryset = PlaylistTrack.objects.all()
    serializer_class = PlaylistTrackSerializer

    def _cache_key(self, playlist_id):
        """Build key used for caching the playlist tracks data."""
        return build_key('playlists-queryset', playlist_id)

    def list(self, request, playlist_id=None):
        """Return a paginated list of playlist track json objects."""
        page = int(request.QUERY_PARAMS.get('page', 1))

        queryset = cache.get(self._cache_key(playlist_id))
        if queryset is None:
            queryset = PlaylistTrack.objects.prefetch_related(
                'track', 'track__artists', 'track__album',
                'track__owner', 'owner'
            ).filter(playlist_id=playlist_id)
            cache.set(self._cache_key(playlist_id), queryset, 86400)

        response = paginate_queryset(
            PaginatedPlaylistTrackSerializer, request, queryset, page)

        return Response(response)

    def create(self, request, *args, **kwargs):
        """Add a track to the database.
        params - track

        Returns a the newly created track as a json object
        """
        track_id = request.POST['track']
        playlist_id = kwargs['playlist_id']

        playlist = Playlist.objects.get(id=playlist_id)
        if (playlist.protection != 'public'
                and request.user != playlist.owner):
            raise PermissionDenied(
                detail='Could not save track. Playlist is marked private.')

        try:
            playlist_track = PlaylistTrack.objects.custom_create(
                track_id, playlist, request.user)
            cache.delete(self._cache_key(playlist_id))
        except:
            raise RecordNotSaved

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
            cache.delete(self._cache_key(playlist_track.playlist.id))
        except:
            raise RecordNotSaved

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
            PlaylistTrack.objects.reset_track_positions(playlist_id)
            cache.delete(self._cache_key(playlist_id))
        except:
            raise RecordDeleteFailed

        return Response({'detail': 'Track removed from playlist'})
