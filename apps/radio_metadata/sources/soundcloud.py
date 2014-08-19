# future imports
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# stdlib imports
import itertools
import logging

# third-party imports
import soundcloud
from django.conf import settings
from django.core.paginator import Paginator


logger = logging.getLogger('rehabradio')


def _search_tracks(query):
    limit = 200
    offset = 0
    tracks = []

    # create a client object with your app credentials
    _client = soundcloud.Client(client_id=settings.SOUNDCLOUD_CLIENT_ID)

    logger.info('Searching: Limit {0}, Offset {1}'.format(limit, offset))
    results = _client.get('/tracks', q=query, limit=limit, offset=offset)
    tracks.append([x.obj for x in results])

    tracks = list(itertools.chain.from_iterable(tracks))
    tracks = [_transform_track(x) for x in tracks]

    return tracks


def _transform_track(track):
    """Transform result into a format that more closely matches our unified API.
    """
    large_artwork = None
    medium_artwork = None
    small_artwork = None

    if track['artwork_url']:
        large_artwork = (track['artwork_url']).replace('large', 't500x500')
        medium_artwork = (track['artwork_url']).replace('large', 't300x300')
        small_artwork = (track['artwork_url']).replace('large', 't67x67')

    transformed_track = dict([
        ('source_type', 'soundcloud'),
        ('source_id', track['id']),
        ('name', track['title']),
        ('duration_ms', track['duration']),
        ('preview_url', track.get('stream_url')),
        ('track_number', 0),
        ('image_small', small_artwork),
        ('image_medium', medium_artwork),
        ('image_large', large_artwork),
    ])
    transformed_track['artists'] = [
        dict([
            ('source_type', 'soundcloud'),
            ('source_id', track['user']['id']),
            ('name', track['user']['username']),
        ]),
    ]
    transformed_track['album'] = None

    return transformed_track


def search_tracks(query, page=1, page_size=50):
    """Search for tracks from Soundcloud.

    musicman uses a unified format to show search results across all supported
    sources. This is a trimmed down version of what is available using direct
    lookups. (see docs for details)

    query (required): string used to search soundcloud
    page: int used to determine which page of results to show
    page_size: maximum number of results returned
    """

    _tracks = _search_tracks(query)
    return Paginator(_tracks, page_size).page(page)


def lookup_track(track_id):
    """Lookup a single track using the soundcloud API
    """
    # create a client object with your app credentials
    _client = soundcloud.Client(client_id=settings.SOUNDCLOUD_CLIENT_ID)
    track = _client.get('/tracks', ids=track_id)[0].obj
    return _transform_track(track)
