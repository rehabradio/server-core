# -*- coding: utf-8 -*-
"""Search/Lookup/Track related views
"""
# stdlib imports
import collections
import datetime
# third-party imports
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
# local imports
from .models import Album, Artist, Track
from .serializers import PaginatedTrackSerializer, TrackSerializer
from .sources import soundcloud
from .sources import spotify
from radio.exceptions import (
    InvalidBackend,
    InvalidLookupType,
    MissingParameter,
    RecordDeleteFailed,
    RecordNotFound,
    RecordNotSaved,
)
from radio.permissions import IsStaffToDelete


def _get_track_data(source_type, source_id):
    """Does a track lookup using the API specified in "source_type".
    Returns a dictionary.
    """
    cache_key = 'search-{0}-{1}-{2}'.format(
        source_type,
        source_id,
        datetime.datetime.utcnow().strftime('%Y%m%d'),
    )

    track_data = cache.get(cache_key)
    if track_data is None:
        if source_type == 'spotify':
            # Query the spotify api for all the track data
            track_data = spotify.lookup_track(source_id)
            # Get or create relational album field
            track_data['album'] = _get_or_create_album(
                track_data['album']
            )
        elif source_type == 'soundcloud':
            # Query the soundcloud api for all the track data
            track_data = soundcloud.lookup_track(source_id)
        else:
            return None
        cache.set(cache_key, track_data)

    return track_data


def _get_or_create_album(album):
    """Get or create an album record from db,
    Returns an Album model reference.
    """
    cache_key = 'album-{0}-{1}-{2}'.format(
        album['source_type'],
        album['source_id'],
        datetime.datetime.utcnow().strftime('%Y%m%d'),
    )

    record = cache.get(cache_key)
    if record is None:
        record, created = Album.objects.get_or_create(
            source_id=album['source_id'],
            source_type=album['source_type'],
            name=album['name'],
        )
        cache.set(cache_key, record)
    return record


def _get_or_create_artists(artists):
    """Get or create artist records from db.
    Returns a list of artist json objects
    """
    records = []
    for (i, artist) in enumerate(artists):
        cache_key = 'artist-{0}-{1}-{2}'.format(
            artist['source_type'],
            artist['source_id'],
            datetime.datetime.utcnow().strftime('%Y%m%d'),
        )

        record = cache.get(cache_key)
        if record is None:
            record, created = Artist.objects.get_or_create(
                source_id=artist['source_id'],
                source_type=artist['source_type'],
                name=artist['name'],
            )
            cache.set(cache_key, record)
        records.append(record)

    return records


def _get_or_create_track(track_data, owner):
    """Saves a track to the db, unless one already exists.
    Returns a track json object
    """
    cache_key = 'track-{0}-{1}-{2}'.format(
        track_data['source_type'],
        track_data['source_id'],
        datetime.datetime.utcnow().strftime('%Y%m%d'),
    )

    record = cache.get(cache_key)
    if record is None:
        try:
            record = Track.objects.get(
                source_id=track_data['source_id'],
                source_type=track_data['source_type'],
            )
        except:
            record = Track.objects.create(
                source_id=track_data['source_id'],
                source_type=track_data['source_type'],
                name=track_data['name'],
                duration_ms=track_data['duration_ms'],
                preview_url=track_data['preview_url'],
                track_number=track_data['track_number'],
                album=track_data['album'],
                image_small=track_data['image_small'],
                image_medium=track_data['image_medium'],
                image_large=track_data['image_large'],
                owner=owner
            )
        cache.set(cache_key, record)

    return record


class MetadataAPIRootView(APIView):
    """The metadata API allows for both search and lookup
    from supported source_types.

    Clients should use the metadata API to retrieve data about available songs.
    The metadata API coerces data from the available source_types into a
    unified format that allows for easy interoperability and addition of
    new source_types in future.
    """

    def get(self, request, format=None):
        response = collections.OrderedDict([
            ('endpoints', collections.OrderedDict([
                ('lookup', reverse('radio-data-lookup-root', request=request)),
                ('search', reverse('radio-data-search-root', request=request)),
                ('tracks', reverse('radio-data-tracks-list', request=request)),
            ])),
        ])
        return Response(response)


class LookupRootView(APIView):
    """The lookup API allows retrieval of metadata from supported source_types.

    Data is cached after initial lookup but is keyed by calendar date to
    ensure that fresh data is fetched at least once per day.

    **Note:** The URLs shown below are examples, to show the standard format of
    the endpoints.
    """

    def get(self, request, format=None):
        response = collections.OrderedDict([
            ('endpoints', collections.OrderedDict([
                ('soundcloud', collections.OrderedDict([
                    (
                        'tracks',
                        reverse(
                            'radio-data-lookup',
                            args=['soundcloud', 153868082],
                            request=request
                        )
                    ),
                ])),
                ('spotify', collections.OrderedDict([
                    (
                        'tracks',
                        reverse(
                            'radio-data-lookup',
                            args=['spotify', '6MeNtkNT4ENE5yohNvGqd4'],
                            request=request
                        )
                    ),
                ])),
            ])),
        ])
        return Response(response)


class LookupView(APIView):
    """Lookup tracks using any configured source_type."""

    def _get_cache_key(self, source_type, source_id):
        """Build key used for caching the lookup data
        """
        return 'mtdt-lkp-{0}-{1}-{2}'.format(
            source_type,
            source_id,
            datetime.datetime.utcnow().strftime('%Y%m%d'),
        )

    def get(self, request, source_type, source_id, format=None):
        """perform metadata lookup
        """
        cache_key = self._get_cache_key(source_type, source_id)
        response = cache.get(cache_key)
        if response is not None:
            return Response(response)

        lookup_func = {
            'soundcloud': soundcloud.lookup_track,
            'spotify': spotify.lookup_track,
        }.get(source_type.lower())
        if lookup_func is None:
            raise InvalidLookupType

        # search using requested source_type and serialize
        try:
            results = lookup_func(source_id)
        except:
            raise RecordNotFound
        response = TrackSerializer(results).data

        # return response to the client
        cache.set(cache_key, response)
        return Response(response)


class SearchRootView(APIView):
    """The search API allows searching for tracks on supported source_types.

    Data is cached after initial lookup but is keyed by calendar date to
    ensure that fresh data is fetched at least once per day.

    **Note:** The URLs shown below are examples, to show the standard format of
    the endpoints.
    """

    def get(self, request, format=None):
        response = collections.OrderedDict([
            ('endpoints', collections.OrderedDict([
                ('soundcloud', collections.OrderedDict([
                    ('tracks', [
                        reverse(
                            'radio-data-search',
                            args=['soundcloud'],
                            request=request
                        ) + '?q=Frederick%20Fringe',
                        reverse(
                            'radio-data-search',
                            args=['soundcloud'],
                            request=request
                        ) + '?q=narsti',
                    ]),
                ])),
                ('spotify', collections.OrderedDict([
                    ('tracks', [
                        reverse(
                            'radio-data-search',
                            args=['spotify'],
                            request=request
                        ) + '?q=Haim',
                        reverse(
                            'radio-data-search',
                            args=['spotify'],
                            request=request
                        ) + '?q=fascination',
                    ]),
                ])),
            ])),
        ])
        return Response(response)


class SearchView(APIView):
    """Search tracks using any configured source_type and a query parameter.
    q -- lookup query (string)
    """

    def get(self, request, source_type, format=None):
        """perform track search and return the results in a consistent format.
        """
        # parse search data from query params
        query = request.QUERY_PARAMS.get('q', '')
        if not query:
            raise MissingParameter
        page = int(request.QUERY_PARAMS.get('page', 1))
        page_size = int(request.QUERY_PARAMS.get('page_size', 20))

        cache_key = u'mtdttrcksrch-{0}-{1}-{2}-{3}-{4}'.format(
            source_type, query, page, page_size,
            datetime.datetime.utcnow().strftime('%Y%m%d'),
        )
        response = cache.get(cache_key)
        if response is not None:
            pass
            return Response(response)

        search_func = {
            'soundcloud': soundcloud.search_tracks,
            'spotify': spotify.search_tracks,
        }.get(source_type.lower())
        if search_func is None:
            raise InvalidBackend

        # search using requested source_type
        results = search_func(query, page, page_size)

        serializer_context = {'request': request}
        serializer = PaginatedTrackSerializer(
            results, context=serializer_context
        )
        response = serializer.data

        # return response to the client
        cache.set(cache_key, response)
        return Response(response)


class TrackViewSet(viewsets.ModelViewSet):
    """CRUD API endpoints that allow managing playlists.
    User must be staff to remove track from database.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = (IsStaffToDelete, permissions.IsAuthenticated)

    def _get_cache_key(self):
        """Build key used for caching the track data."""
        return 'tracklist-{0}'.format(
            datetime.datetime.utcnow().strftime('%Y%m%d'),
        )

    def list(self, request, pk=None):
        """Return a paginated list of track json objects."""
        cache_key = self._get_cache_key()
        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = Track.objects.prefetch_related(
                'artists',
                'album',
                'owner',
            ).all()
            cache.set(cache_key, queryset, 86400)

        paginator = Paginator(queryset, 20)

        page = request.QUERY_PARAMS.get('page')
        try:
            tracks = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            tracks = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            tracks = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        serializer = PaginatedTrackSerializer(
            tracks, context=serializer_context
        )
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Add a track to the database.
        params - source_type, source_id

        Returns a the newly created track as a json object
        """
        try:
            track_data = _get_track_data(
                request.POST['source_type'],
                request.POST['source_id']
            )
        except:
            raise RecordNotFound

        if track_data is None:
            raise RecordNotFound

        try:
            track = _get_or_create_track(track_data, self.request.user)
            _get_or_create_artists(track_data['artists'])
        except:
            raise RecordNotSaved

        cache.delete(self._get_cache_key())

        serializer = TrackSerializer(track)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Removes track from database, returning a detail reponse."""
        try:
            track = Track.objects.get(id=kwargs['pk'])
        except:
            raise RecordNotFound

        try:
            track.delete()
        except:
            raise RecordDeleteFailed

        cache.delete(self._get_cache_key())

        return Response({'detail': 'Track successfully removed'})

    def pre_save(self, obj):
        """Remove the cached track list after a database record is updated."""
        cache.delete(self._get_cache_key())
