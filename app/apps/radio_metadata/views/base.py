# -*- coding: utf-8 -*-
"""Search/Lookup/Track related views
"""
# stdlib imports
import collections

# third-party imports
from django.conf import settings
from radiobabel import SpotifyClient, SoundcloudClient, YoutubeClient
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


spotify_client = SpotifyClient()
soundcloud_client = SoundcloudClient(settings.SOUNDCLOUD_CLIENT_ID)
youtube_client = YoutubeClient()


def build_client(source_type):
    """Builds the thrid party api client based on the given source type."""
    source_client = {
        'soundcloud': soundcloud_client,
        'spotify': spotify_client,
        'youtube': youtube_client,
    }.get(source_type.lower())

    return source_client


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
                ('user', reverse('radio-data-user-root', request=request)),
            ])),
        ])
        return Response(response)
