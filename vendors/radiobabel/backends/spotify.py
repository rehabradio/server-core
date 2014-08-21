# future imports
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# stdlib imports
import logging

# third-party imports
import requests

# local imports
from radiobabel.errors import TrackNotFound


logger = logging.getLogger('radiobabel.backends.spotify')


def _make_request(url, params=None):
    """Make a HTTP request to the spotify API using the requests library
    """
    response = requests.get(url, params=params)
    # raise an exception if 400 <= response.status_code <= 599
    response.raise_for_status()
    return response.json()


def _transform_search_response(search_results, offset):
    """Transform a result returned from the spotify API into a format we
    can return to clients/use to populate the database.
    """
    _track_list = [None for x in xrange(search_results['tracks']['total'])]
    for idx, track in enumerate(search_results['tracks']['items']):
        transformed_track = _transform_track(track)
        _track_list[offset + idx] = transformed_track
    return _track_list


def _transform_track(track):
    """Transform result into a format that more
    closely matches our unified API.
    """
    transformed_track = dict([
        ('source_type', 'spotify'),
        ('source_id', track['id']),
        ('name', track['name']),
        ('duration_ms', track['duration_ms']),
        ('preview_url', track['preview_url']),
        ('track_number', track['track_number']),
        ('image_small', None),
        ('image_medium', None),
        ('image_large', None),
    ])
    transformed_track['artists'] = []
    for artist in track.get('artists', []):
        transformed_track['artists'].append(dict([
            ('source_type', 'spotify'),
            ('source_id', artist['id']),
            ('name', artist['name']),
        ]))
    transformed_track['album'] = dict([
        ('source_type', 'spotify'),
        ('source_id', track['album']['id']),
        ('name', track['album']['name']),
    ])
    if track['album']['images']:
        transformed_track['image_large'] = track['album']['images'][0]['url']
        try:
            transformed_track['image_medium'] = \
                track['album']['images'][1]['url']
        except:
            pass
        try:
            transformed_track['image_small'] = \
                track['album']['images'][2]['url']
        except:
            pass

    return transformed_track


class SpotifyClient(object):

    def track(self, track_id):
        """Lookup an individual track using the Spotify Web API

        radiobabel uses a unified format to show lookup results across all
        supported sources. This allows simple interaction for clients and easy
        implementation of a unified search API in future.

        track_id (required): id of the Spotify track to retrieve metadata for.
        """
        url = 'https://api.spotify.com/v1/tracks/{0}'.format(track_id)
        logger.info('Track lookup: {0}'.format(track_id))
        try:
            track = _make_request(url)
        except IndexError:
            raise TrackNotFound('Spotify: {0}'.format(track_id))

        return _transform_track(track)

    def search(self, query, limit=20, offset=0):
        """Search for tracks using the spotify API
        """
        logger.info('Searching: Limit {0}, Offset {1}'.format(limit, offset))

        # Max limit for the spotify api is 20
        if limit > 20:
            limit = 20

        params = {'q': query, 'type': 'track',
                  'limit': limit, 'offset': offset}
        response = _make_request('https://api.spotify.com/v1/search', params)
        tracks = _transform_search_response(response, offset)

        return tracks
