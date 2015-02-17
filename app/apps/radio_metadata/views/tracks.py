# -*- coding: utf-8 -*-
"""Search/Lookup/Track related views
"""
# third-party imports
from django.core.cache import cache
from rest_framework import permissions, viewsets
from rest_framework.response import Response

# local imports
from .base import build_client
from ..models import Track
from ..serializers import PaginatedTrackSerializer
from ..serializers import TrackSerializer
from radio.exceptions import RecordDeleteFailed
from radio.exceptions import RecordNotFound
from radio.exceptions import RecordNotSaved
from radio.exceptions import RecordNoLongerExists
from radio.permissions import IsStaffToDelete
from radio.utils.cache import build_key
from radio.utils.pagination import paginate_queryset


def _get_track_data(source_type, source_id):
    """Does a track lookup using the thrid party api client.
    Returns a dictionary.
    """
    cache_key = build_key('track_lookup', source_type, source_id)

    track_data = cache.get(cache_key)
    if track_data is None:
        source_client = build_client(source_type)
        track_data = source_client.lookup_track(source_id)

        cache.set(cache_key, track_data, 86400)

    return track_data


def track_exists(track_id):
    """Looks up the track using the thrid party client
    to ensure the track has not be removed from source.
    """
    try:
        track = Track.objects.get(pk=track_id)
    except:
        raise RecordNotFound('The track could not be found.')

    source_client = build_client(track.source_type)
    try:
        source_client.lookup_track(track.source_id)
    except:
        cache.delete(build_key('tracklist-queryset'))
        track.delete()

        raise RecordNoLongerExists


def get_associated_track(source_id, source_type, user):
    """Fetches a random track based on a given track.
    """
    source_client = build_client(source_type)
    track = source_client.fetch_associated_track(source_id)

    try:
        track = Track.objects.cached_get_or_create(track, user)
    except:
        raise RecordNotSaved

    serializer = TrackSerializer(track)
    return serializer.data


class TrackViewSet(viewsets.ModelViewSet):
    """CRUD API endpoints that allow managing playlists.
    User must be staff to remove track from database.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = (IsStaffToDelete, permissions.IsAuthenticated)

    cache_key = build_key('tracklist-queryset')

    def list(self, request, pk=None):
        """Return a paginated list of track json objects."""
        page = int(request.QUERY_PARAMS.get('page', 1))

        queryset = cache.get(self.cache_key)
        if queryset is None:
            queryset = Track.objects.prefetch_related(
                'artists', 'album', 'owner').all()
            cache.set(self.cache_key, queryset, 86400)

        response = paginate_queryset(
            PaginatedTrackSerializer, request, queryset, page)

        return Response(response)

    def create(self, request, *args, **kwargs):
        """Add a track to the database.
        params - source_type, source_id

        Returns a the newly created track as a json object
        """
        try:
            track_data = _get_track_data(
                request.POST['source_type'], request.POST['source_id'])
        except:
            raise RecordNotFound
        else:
            if track_data is None:
                raise RecordNotFound

        try:
            cache.delete(self.cache_key)
            track = Track.objects.cached_get_or_create(
                track_data, self.request.user)
        except:
            raise RecordNotSaved

        serializer = TrackSerializer(track)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Removes track from database, returning a detail reponse."""
        try:
            track = Track.objects.get(id=kwargs['pk'])
        except:
            raise RecordNotFound

        try:
            cache.delete(self.cache_key)
            track.delete()
        except:
            raise RecordDeleteFailed

        return Response({'detail': 'Track successfully removed'})
