# future imports
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# stdlib imports
import datetime
import itertools
import logging

# third-party imports
import soundcloud
from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator


logger = logging.getLogger('rehabradio')


def _search_tracks(query):

    key_params = {'q': query, 'd': datetime.datetime.utcnow().strftime('%Y%m%d')}
    cache_key = 'sndcldsrch-{q}-{d}'.format(**key_params)

    tracks = cache.get(cache_key)
    if tracks is not None:
        return tracks

    limit = 200
    offset = 0
    tracks = []

    # create a client object with your app credentials
    _client = soundcloud.Client(client_id=settings.SOUNDCLOUD_CLIENT_ID)

    # keep fetching results until there aren't any more, this does add some
    # overhead to initial searches, but with some caching i think it'll be
    # worth doing it this way.
    while True:
        logger.info('Searching: Limit {0}, Offset {1}'.format(limit, offset))
        results = _client.get('/tracks', q=query, limit=limit, offset=offset)
        tracks.append([x.obj for x in results])
        if len(results) < limit:
            break
        offset += limit

    tracks = list(itertools.chain.from_iterable(tracks))
    tracks = [_transform_track(x) for x in tracks]

    cache.set(cache_key, tracks)
    return tracks


def _transform_track(track):
    """Transform result into a format that more closely matches our unified API.
    """
    small_artwork = str(track['artwork_url']).replace('large', 't500x500')
    medium_artwork = str(track['artwork_url']).replace('large', 't300x300')
    large_artwork = str(track['artwork_url']).replace('large', 't67x67')

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
