# -*- coding: utf-8 -*-
"""Search/Lookup/Track related views
"""
# stdlib imports
import collections

# third-party imports
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

# local imports
from .base import build_client
from ..serializers import PaginatedTrackSerializer, TrackSerializer
from radio.exceptions import InvalidBackend, OauthFailed, ThridPartyOauthRequired
from radio.utils.cache import build_key
from radio.utils.pagination import paginate_queryset


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
                    )),
                    ('youtube', reverse(
                        'radio-data-user-auth',
                        args=['youtube'],
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
                    )),
                    ('youtube', reverse(
                        'radio-data-user-playlists',
                        args=['youtube'],
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
        elif source_type.lower() == 'youtube':
            source_client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
            source_client_secret = settings.GOOGLE_OAUTH2_CLIENT_SECRET
        else:
            raise InvalidBackend

        cache_key = build_key('user-credentials', source_type, request.user.id)
        credentials = cache.get(cache_key)
        if credentials:
            return Response(credentials)

        source_client = build_client(source_type)
        if source_client is None:
            raise InvalidBackend

        try:
            # Prompt user to login
            if auth_code is None:
                redirect_url = source_client.login_url(
                    request.build_absolute_uri(request.path),
                    source_client_id,
                    source_client_secret
                )
                return redirect(redirect_url)
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

    queryset = None
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

        source_client = build_client(source_type)
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

        source_client = build_client(source_type)
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
