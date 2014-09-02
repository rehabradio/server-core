# -*- coding: utf-8 -*-
"""Search/Lookup/Track related views
"""
# stdlib imports
import collections

# third-party imports
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect
from radiobabel import SpotifyClient, SoundcloudClient
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

# local imports
from .models import Album, Artist, Track
from .serializers import PaginatedTrackSerializer, TrackSerializer
from radio.exceptions import (
    InvalidBackend, MissingParameter, OauthFailed, ThridPartyOauthRequired,
    RecordDeleteFailed, RecordNotFound, RecordNotSaved)
from radio.permissions import IsStaffToDelete
from radio.utils.cache import build_key
from radio.utils.pagination import paginate_queryset


spotify_client = SpotifyClient()
soundcloud_client = SoundcloudClient(settings.SOUNDCLOUD_CLIENT_ID)


def _build_client(source_type):
    source_client = {
        'soundcloud': soundcloud_client,
        'spotify': spotify_client,
    }.get(source_type.lower())

    return source_client


def _get_track_data(source_type, source_id):
    """Does a track lookup using the API specified in "source_type".
    Returns a dictionary.
    """
    cache_key = build_key('search', source_type, source_id)

    track_data = cache.get(cache_key)
    if track_data is None:
        source_client = _build_client(source_type)
        track_data = source_client.lookup_track(source_id)

        if source_type == 'spotify':
            # Get or create relational album field
            track_data['album'] = _get_or_create_album(track_data['album'])

        cache.set(cache_key, track_data)

    return track_data


def _get_or_create_album(album):
    """Get or create an album record from db,
    Returns an Album model reference.
    """
    cache_key = build_key('album', album['source_type'], album['source_id'])

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
        cache_key = build_key('artist', artist['source_type'], artist['source_id'])

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


def _get_or_create_track(track, owner):
    """Saves a track to the db, unless one already exists.
    Returns a track json object
    """
    cache_key = build_key('artist', track['source_type'], track['source_id'])

    record = cache.get(cache_key)
    if record is None:
        try:
            record = Track.objects.get(
                source_id=track['source_id'],
                source_type=track['source_type'],
            )
        except:
            record = Track.objects.create(
                source_id=track['source_id'],
                source_type=track['source_type'],
                name=track['name'],
                duration_ms=track['duration_ms'],
                preview_url=track['preview_url'],
                track_number=track['track_number'],
                album=track['album'],
                image_small=track['image_small'],
                image_medium=track['image_medium'],
                image_large=track['image_large'],
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
                ('user', reverse('radio-data-user-root', request=request)),
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
                    ('tracks', reverse(
                        'radio-data-lookup',
                        args=['soundcloud', 153868082],
                        request=request
                    )),
                ])),
                ('spotify', collections.OrderedDict([
                    ('tracks', reverse(
                        'radio-data-lookup',
                        args=['spotify', '6MeNtkNT4ENE5yohNvGqd4'],
                        request=request
                    )),
                ])),
            ])),
        ])
        return Response(response)


class LookupView(APIView):
    """Lookup tracks using any configured source_type."""

    def get(self, request, source_type, source_id, format=None):
        """perform metadata lookup
        """
        cache_key = build_key('mtdt-lkp', source_type, source_id)
        response = cache.get(cache_key)
        if response is not None:
            return Response(response)

        source_client = _build_client(source_type)
        if source_client is None:
            raise InvalidBackend

        # search using requested source_type and serialize
        try:
            results = source_client.lookup_track(source_id)
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

        cache_key = build_key('mtdttrcksrch', source_type, query, page)
        response = cache.get(cache_key)

        if response is not None:
            return Response(response)

        source_client = _build_client(source_type)
        if source_client is None:
            raise InvalidBackend

        # search using requested source_type
        offset = (page-1)*20
        queryset = source_client.search_tracks(query, page*200, offset)
        response = paginate_queryset(
            PaginatedTrackSerializer, request, queryset, page)

        cache.set(cache_key, response)
        return Response(response)


class UserRootView(APIView):
    """The user playlist loopup API allows retrieval of metadata
    from supported source_types.

    Data is cached after initial lookup but is keyed by calendar date to
    ensure that fresh data is fetched at least once per day.

    **Note:** The URLs shown below are examples, to show the standard format of
    the endpoints.
    """

    def get(self, request, format=None):
        response = collections.OrderedDict([
            ('endpoints', collections.OrderedDict([
                ('oauth', collections.OrderedDict([
                    ('soundcloud', reverse(
                        'radio-data-user-auth',
                        args=['soundcloud'],
                        request=request
                    )),
                    ('spotify', reverse(
                        'radio-data-user-auth',
                        args=['spotify'],
                        request=request
                    ))
                ])),
                ('favourites', collections.OrderedDict([
                    ('soundcloud', reverse(
                        'radio-data-user-favorites',
                        args=['soundcloud'],
                        request=request
                    )),
                    ('spotify', reverse(
                        'radio-data-user-favorites',
                        args=['spotify'],
                        request=request
                    ))
                ])),
                ('playlists', collections.OrderedDict([
                    ('soundcloud', reverse(
                        'radio-data-user-playlists',
                        args=['soundcloud'],
                        request=request
                    )),
                    ('spotify', reverse(
                        'radio-data-user-playlists',
                        args=['spotify'],
                        request=request
                    ))
                ])),
            ])),
        ])
        return Response(response)


class UserAuthView(APIView):
    """Authenticate user to use oauth on a given service (spotify/soundcloud).
    """

    def get(self, request, source_type, format=None):
        if source_type.lower() == 'spotify':
            source_client_id = settings.SPOTIFY_CLIENT_ID
            source_client_secret = settings.SPOTIFY_CLIENT_SECRET
        elif source_type.lower() == 'soundcloud':
            source_client_id = settings.SOUNDCLOUD_CLIENT_ID
            source_client_secret = settings.SOUNDCLOUD_CLIENT_SECRET
        else:
            raise InvalidBackend

        cache_key = build_key('user-credentials', source_type, request.user.id)
        credentials = cache.get(cache_key)

        if credentials:
            return Response(credentials)

        auth_code = request.QUERY_PARAMS.get('code', None)

        source_client = _build_client(source_type)
        if source_client is None:
            raise InvalidBackend

        try:
            # Prompt user to login
            if auth_code is None:
                redirect_uri = source_client.login_url(
                    request.build_absolute_uri(request.path),
                    source_client_id,
                    source_client_secret
                )
                return redirect(redirect_uri)
            # Else exchange the auth code for an oauth token
            else:
                credentials = source_client.exchange_code(
                    auth_code,
                    request.build_absolute_uri(request.path),
                    source_client_id,
                    source_client_secret
                )
        except:
            raise OauthFailed

        cache.set(
            cache_key, credentials,
            credentials['auth']['expires_in'] * 100
        )

        return Response(credentials)


class UserPlaylistViewSet(viewsets.GenericViewSet):
    """Lookup tracks using any configured source_type."""

    def list(self, request, source_type, format=None):
        """Perform metadata lookup on the user playlists.
        """
        cache_key = build_key('user-playlists', source_type, request.user.id)

        playlists = cache.get(cache_key)
        if playlists:
            return Response(playlists)

        oauth_cache_key = build_key(
            'user-credentials', source_type, request.user.id)
        credentials = cache.get(oauth_cache_key)

        if credentials is None:
            raise ThridPartyOauthRequired

        source_client = _build_client(source_type)
        if source_client is None:
            raise InvalidBackend

        playlists = source_client.playlists(
            credentials['user']['id'], credentials['auth']['access_token'])
        cache.set(cache_key, playlists)

        return Response(playlists)

    def retrieve(self, request, source_type, playlist_id, format=None):
        """Perform metadata lookup on the user playlists.
        """
        page = int(request.QUERY_PARAMS.get('page', 1))

        cache_key = build_key('user-playlist-tracks', source_type, playlist_id)
        response = cache.get(cache_key)
        if response:
            return Response(response)

        oauth_cache_key = build_key(
            'user-credentials', source_type, request.user.id)
        credentials = cache.get(oauth_cache_key)

        if credentials is None:
            raise ThridPartyOauthRequired

        source_client = _build_client(source_type)
        if source_client is None:
            raise InvalidBackend

        # search using requested source_type
        offset = (page-1)*20
        queryset = source_client.playlist_tracks(
            playlist_id, credentials['user']['id'],
            credentials['auth']['access_token'], page*200, offset)

        response = paginate_queryset(
            PaginatedTrackSerializer, request, queryset, page)

        cache.set(cache_key, response)
        return Response(response)


class UserFavoritesViewSet(viewsets.GenericViewSet):
    """Lookup tracks using any configured source_type."""

    def list(self, request, source_type, format=None):
        """Perform metadata lookup on the user playlists."""
        if source_type == 'spotify':
            return Response({'detail': 'Spotify currently not enabled'})

        page = int(request.QUERY_PARAMS.get('page', 1))

        cache_key = build_key(
            'user-favorite-tracks', source_type, request.user.id)
        response = cache.get(cache_key)
        if response:
            return Response(response)

        oauth_cache_key = build_key(
            'user-credentials', source_type, request.user.id)
        credentials = cache.get(oauth_cache_key)

        if credentials is None:
            raise ThridPartyOauthRequired

        source_client = _build_client(source_type)
        if source_client is None:
            raise InvalidBackend

        # search using requested source_type
        offset = (page-1)*20
        queryset = source_client.favorites(
            credentials['user']['id'],
            credentials['auth']['access_token'], page*200, offset)

        response = paginate_queryset(
            PaginatedTrackSerializer, request, queryset, page)

        cache.set(cache_key, response)
        return Response(response)


class TrackViewSet(viewsets.ModelViewSet):
    """CRUD API endpoints that allow managing playlists.
    User must be staff to remove track from database.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = (IsStaffToDelete, permissions.IsAuthenticated)

    cache_key = build_key('tracklist')

    def list(self, request, pk=None):
        """Return a paginated list of track json objects."""
        page = int(request.QUERY_PARAMS.get('page', 1))

        response = cache.get(self.cache_key)
        if response:
            return Response(response)

        queryset = Track.objects.prefetch_related(
            'artists', 'album', 'owner',).all()

        response = paginate_queryset(
            PaginatedTrackSerializer, request, queryset, page)

        cache.set(self.cache_key, response)
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
            track = _get_or_create_track(track_data, self.request.user)
            _get_or_create_artists(track_data['artists'])
            serializer = TrackSerializer(track)
            cache.delete(self.cache_key)
        except:
            raise RecordNotSaved

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Removes track from database, returning a detail reponse."""
        try:
            track = Track.objects.get(id=kwargs['pk'])
        except:
            raise RecordNotFound

        try:
            track.delete()
            cache.delete(self.cache_key)
        except:
            raise RecordDeleteFailed

        return Response({'detail': 'Track successfully removed'})

    def pre_save(self, obj):
        """Remove the cached track list after a database record is updated."""
        cache.delete(self.cache_key)
