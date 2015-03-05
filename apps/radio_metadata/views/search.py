# -*- coding: utf-8 -*-
"""Search/Lookup/Track related views
"""
# stdlib imports
import collections

# third-party imports
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

# local imports
from .base import build_client
from ..serializers import PaginatedTrackSerializer
from radio.exceptions import InvalidBackend, MissingParameter
from radio.utils.cache import build_key
from radio.utils.pagination import paginate_queryset


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
        limit = 20
        offset = (page-1)*limit

        query = request.QUERY_PARAMS.get('q', '')
        if not query:
            raise MissingParameter

        cache_key = build_key('mtdttrcksrch', source_type, query, page)
        response = cache.get(cache_key)
        if response is not None:
            return Response(response)

        source_client = build_client(source_type)
        if source_client is None:
            raise InvalidBackend

        queryset = source_client.search_tracks(query, limit, offset)
        response = paginate_queryset(
            PaginatedTrackSerializer, request, queryset, page)

        response['query'] = query

        cache.set(cache_key, response, 86400)
        return Response(response)
