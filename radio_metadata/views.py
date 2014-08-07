# -*- coding: utf-8 -*-
"""Search/Lookup related views
"""
# stdlib imports
import collections
import datetime

# third-party imports
from django.core.cache import cache
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

# local imports
from .models import Album, Artist, Track
from .serializers import PaginatedTrackSerializer, TrackSerializer
from .sources import soundcloud
from .sources import spotify

from radio.custom_exceptions import InvalidBackend, MissingParameter


def _getTrackData(source_type, source_id):
    """
    Does a track lookup using the API specified in "source_type"
    Returns a dictionary
    """
    if source_type == 'spotify':
        # Query the spotify api for all the track data
        track_data = spotify.lookup_track(source_id)
        # Get or create relational album field
        track_data['album'] = _getOrCreateAlbum(
            track_data['album'],
            'spotify'
        )
    elif source_type == 'soundcloud':
        # Query the soundcloud api for all the track data
        track_data = soundcloud.lookup_track(source_id)
    else:
        raise InvalidBackend

    return track_data


def _getOrCreateAlbum(album, source_type):
    """
    Get or create an album record from db,
    Returns an Album model reference
    """
    record, created = Album.objects.get_or_create(
        source_id=album['source_id'],
        source_type=source_type,
        name=album['name'],
    )
    return record


def _getOrCreateArtists(artists, source_type):
    """
    Get or create artist records from db,
    Returns a list of Artist model references
    """
    artistModels = []
    for (i, artist) in enumerate(artists):
        record, created = Artist.objects.get_or_create(
            source_id=artist['source_id'],
            source_type=source_type,
            name=artist['name'],
        )
        artistModels.append(record)

    return artistModels


def _getOrCreateTrack(track_data, owner):
    """
    Saves a track to the db, unless one already exists
    Returns reference to Track model reference
    """
    track, created = Track.objects.get_or_create(
        source_id=track_data['source_id'],
        source_type=track_data['source_type'],
        name=track_data['name'],
        duration_ms=track_data['duration_ms'],
        preview_url=track_data['preview_url'],
        track_number=track_data['track_number'],
        album=track_data['album'],
    )
    if created:
        track.image_small = track_data['image_small'],
        track.image_medium = track_data['image_medium'],
        track.image_large = track_data['image_large'],
        track.owner = owner
        track.save()

    return {'created': created, 'track': track}


class MetadataAPIRootView(APIView):
    """
    The metadata API allows for both search and lookup from supported backends.

    Clients should use the metadata API to retrieve data about available songs.
    The metadata API coerces data from the available backends into a unified
    format that allows for easy interoperability and addition of new backends
    in future.
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
    """
    The lookup API allows retrieval of metadata from supported backends.

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
    """Lookup tracks/artists/albums using any configured backend
    """

    def _get_cache_key(self, backend, pk):
        """Build key used for caching the lookup data
        """
        return 'mtdt-lkp-{0}-{1}-{2}'.format(
            backend, pk, datetime.datetime.utcnow().strftime('%Y%m%d'),
        )

    def get(self, request, backend, pk, format=None):
        """perform metadata lookup
        """
        cache_key = self._get_cache_key(backend, pk)
        response = cache.get(cache_key)
        if response is not None:
            return Response(response)

        lookup_func = {
            'soundcloud': soundcloud.lookup_track,
            'spotify': spotify.lookup_track,
        }.get(backend.lower())
        if lookup_func is None:
            raise InvalidBackend

        # search using requested backend and serialize
        results = lookup_func(pk)
        response = TrackSerializer(results).data

        # return response to the client
        cache.set(cache_key, response)
        return Response(response)


class SearchRootView(APIView):
    """
    The search API allows searching for tracks on supported backends.

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
    """Search tracks using any configured backend
    """

    def get(self, request, backend, format=None):
        """perform track search and return the results in a consistent format
        """
        # parse search data from query params
        query = request.QUERY_PARAMS.get('q', '')
        if not query:
            raise MissingParameter
        page = int(request.QUERY_PARAMS.get('page', 1))
        page_size = int(request.QUERY_PARAMS.get('page_size', 20))

        cache_key = u'mtdttrcksrch-{0}-{1}-{2}-{3}-{4}'.format(
            backend, query, page, page_size,
            datetime.datetime.utcnow().strftime('%Y%m%d'),
        )
        response = cache.get(cache_key)
        if response is not None:
            pass
            return Response(response)

        search_func = {
            'soundcloud': soundcloud.search_tracks,
            'spotify': spotify.search_tracks,
        }.get(backend.lower())
        if search_func is None:
            raise InvalidBackend

        # search using requested backend
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
    """
    CRUD API endpoints that allow managing playlists.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    def create(self, request, *args, **kwargs):
        # Use api to fetch track information
        post_data = request.POST
        try:
            track_data = _getTrackData(
                post_data['source_type'],
                post_data['source_id']
            )
        except:
            response = {
                'message': 'Track could not be found',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        # Save the track
        try:
            trackObj = _getOrCreateTrack(track_data, self.request.user)
            track = trackObj['track']
        except:
            response = {
                'message': 'Track could not be saved',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        # Save the track artists
        try:
            _getOrCreateArtists(
                track_data['artists'],
                post_data['source_type']
            )
        except:
            response = {
                'message': 'Artists could not be saved',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        new_track = Track.objects.filter(id=track.id).values()[0]

        return Response(new_track)

    # Set user id, for each record saved
    def pre_save(self, obj):
        obj.owner = self.request.user
