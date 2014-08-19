"""Simple interface to the Spotify Web API
"""
# future imports
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# third-party imports
import requests
from django.core.paginator import Paginator


__all__ = ['search_tracks']


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


def search_tracks(query, page=1, page_size=20):
    """Search for tracks from Spotify.

    musicman uses a unified format to show search results across all supported
    sources. This is a trimmed down version of what is available using direct
    lookups. (see docs for details)

    query (required): string used to search spotify
    page: int used to determine which page of results to show
    page_size: maximum number of results returned
    """

    _offset = (int(page) - 1) * page_size
    _params = {'q': query, 'type': 'track', 'limit': page_size, 'offset': _offset}
    _response = _make_request('https://api.spotify.com/v1/search', _params)
    _tracks = _transform_search_response(_response, _offset)
    return Paginator(_tracks, page_size).page(page)


def _transform_track(track):
    """Transform the result of a track lookup from the raw format returned by
    the Spotify API into something that better fits our unified API.

    response (required): dictionary of data returned from the Spotify web API
    """
    transformed_track = dict([
        ('source_type', 'spotify'),
        ('source_id', track['id']),
        ('name', track['name']),
        ('duration_ms', track['duration_ms']),
        ('preview_url', track['preview_url']),
        ('track_number', track['track_number']),
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
        transformed_track['image_small'] = track['album']['images'][0]['url']
        try:
            transformed_track['image_medium'] = track['album']['images'][1]['url']
        except:
            transformed_track['image_medium'] = transformed_track['image_small']

        try:
            transformed_track['image_large'] = track['album']['images'][2]['url']
        except:
            transformed_track['image_large'] = transformed_track['image_medium']
    else:
        transformed_track['image_small'] = None
        transformed_track['image_medium'] = None
        transformed_track['image_large'] = None

    return transformed_track


def lookup_track(track_id):
    """Lookup an individual track using the Spotify Web API

    musicman uses a unified format to show lookup results across all supported
    sources. This allows simple interaction for clients and easy implementation
    of a unified search API in future.

    track_id (required): id of the Spotify track to retrieve metadata for.
    """
    url = 'https://api.spotify.com/v1/tracks/{0}'.format(track_id)
    response = _make_request(url)
    return _transform_track(response)
