# -*- coding: utf-8 -*-
"""Search/Lookup/Track related views
"""
# stdlib imports
import collections

# third-party imports
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect
from radiobabel import SpotifyClient, SoundcloudClient, YoutubeClient
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

# local imports
from .models import Track
from .serializers import PaginatedTrackSerializer, TrackSerializer
from radio.exceptions import (
    InvalidBackend, MissingParameter, OauthFailed, ThridPartyOauthRequired,
    RecordDeleteFailed, RecordNotFound, RecordNotSaved)
from radio.permissions import IsStaffToDelete
from radio.utils.cache import build_key
from radio.utils.pagination import paginate_queryset


spotify_client = SpotifyClient()
soundcloud_client = SoundcloudClient(settings.SOUNDCLOUD_CLIENT_ID)
youtube_client = YoutubeClient(settings.GOOGLE_OAUTH2_CLIENT_ID)


def _build_client(source_type):
    """Builds the thrid party api client based on the given source type."""
    source_client = {
        'youtube': youtube_client,
        'soundcloud': soundcloud_client,
        'spotify': spotify_client,
    }.get(source_type.lower())

    return source_client


def _get_track_data(source_type, source_id):
    """Does a track lookup using the thrid party api client.
    Returns a dictionary.
    """
    cache_key = build_key('search', source_type, source_id)

    track_data = cache.get(cache_key)
    if track_data is None:
        source_client = _build_client(source_type)
        track_data = source_client.lookup_track(source_id)

        cache.set(cache_key, track_data, 86400)

    return track_data


def get_associated_track(source_id, source_type, user):
    source_client = _build_client(source_type)
    track = source_client.fetch_associated_track(source_id)

    try:
        track = Track.objects.cached_get_or_create(track, user)
    except:
        raise RecordNotSaved

    serializer = TrackSerializer(track)
    return serializer.data


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
                ('youtube', collections.OrderedDict([
                    ('tracks', reverse(
                        'radio-data-lookup',
                        args=[
                            'youtube',
                            'StTqXEQ2l-Y'
                        ],
                        request=request
                    )),
                ])),
            ])),
        ])
        return Response(response)


class LookupView(APIView):
    """Lookup tracks using any configured source_type."""

    def get(self, request, source_type, source_id, format=None):
        cache_key = build_key('mtdt-lkp', source_type, source_id)
        response = cache.get(cache_key)
        if response is not None:
            return Response(response)

        source_client = _build_client(source_type)
        if source_client is None:
            raise InvalidBackend

        try:
            results = source_client.lookup_track(source_id)
        except:
            raise RecordNotFound

        response = TrackSerializer(results).data
        cache.set(cache_key, response, 86400)
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
                ('youtube', collections.OrderedDict([
                    ('tracks', [
                        reverse(
                            'radio-data-search',
                            args=['youtube'],
                            request=request
                        ) + '?q=everything%20is%20awesome',
                        reverse(
                            'radio-data-search',
                            args=['youtube'],
                            request=request
                        ) + '?q=foo%20fighters',
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
        page = int(request.QUERY_PARAMS.get('page', 1))

        query = request.QUERY_PARAMS.get('q', '')
        if not query:
            raise MissingParameter

        cache_key = build_key('mtdttrcksrch', source_type, query, page)
        response = cache.get(cache_key)
        if response is not None:
            return Response(response)

        source_client = _build_client(source_type)
        if source_client is None:
            raise InvalidBackend

        offset = (page-1)*20
        queryset = source_client.search_tracks(query, page*200, offset)
        response = paginate_queryset(
            PaginatedTrackSerializer, request, queryset, page)

        cache.set(cache_key, response, 86400)
        return Response(response)


class UserRootView(APIView):
    """The user loopup API allows authentication and
    retrieval of metadata from supported source_types.

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
    """Authenticate user to use oauth on a given service."""

    def get(self, request, source_type, format=None):
        auth_code = request.QUERY_PARAMS.get('code', None)

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
            cache_key, credentials, credentials['auth']['expires_in'])

        return Response(credentials)


class UserPlaylistViewSet(viewsets.GenericViewSet):
    """Lookup tracks using any configured source_type."""

    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    def list(self, request, source_type, format=None):
        """Perform metadata lookup on the user playlists."""
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

        response = source_client.playlists(
            credentials['user']['id'], credentials['auth']['access_token'])
        cache.set(cache_key, response, 86400)

        return Response(response)

    def retrieve(self, request, source_type, playlist_id, format=None):
        """Perform metadata lookup on the user playlists."""
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

        cache.set(cache_key, response, 86400)
        return Response(response)


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
            track = Track.objects.cached_get_or_create(
                track_data, self.request.user)
        except:
            raise RecordNotSaved

        serializer = TrackSerializer(track)
        cache.delete(self.cache_key)

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
