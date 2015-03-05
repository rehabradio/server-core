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
from ..serializers import TrackSerializer
from radio.exceptions import InvalidBackend, RecordNotFound
from radio.utils.cache import build_key


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

        source_client = build_client(source_type)
        if source_client is None:
            raise InvalidBackend

        try:
            results = source_client.lookup_track(source_id)
        except:
            raise RecordNotFound

        response = TrackSerializer(results).data
        cache.set(cache_key, response, 86400)
        return Response(response)
