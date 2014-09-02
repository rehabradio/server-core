# future imports
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# stdlib imports
import logging

# third-party imports
import soundcloud

# local imports
from radiobabel.errors import TrackNotFound, PlaylistNotFound


logger = logging.getLogger('radiobabel.backends.soundcloud')


def _transform_track(track):
    """Transform result into a format that
    more closely matches our unified API.
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


def _transform_playlist(playlist):
    """Transform result into a format that more
    closely matches our unified API.
    """
    transformed_playlist = dict([
        ('source_type', 'soundcloud'),
        ('source_id', playlist.id),
        ('name', playlist.title),
        ('tracks', playlist.track_count),
    ])
    return transformed_playlist


class SoundcloudClient(object):

    def __init__(self, client_id):
        """Initialise soundcloud API client.
        """
        self.client = soundcloud.Client(client_id=client_id)

    def login_url(self, callback_url, client_id, client_secret):
        """Generates a login url, for the user to authenticate the app."""
        self.client = soundcloud.Client(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=callback_url
        )
        return self.client.authorize_url()

    def exchange_code(self, code, callback_url, client_id, client_secret):
        """Fetch auth and user data from the soundcloud api

        Returns a dictionary of a auth and user object.
        """
        auth_obj = self.client.exchange_token(code)
        try:
            expires_in = auth_obj.expires_in
            refresh_token = auth_obj.refresh_token
        except:
            expires_in = 864000
            refresh_token = None

        auth_data = {
            'access_token': auth_obj.access_token,
            'refresh_token': refresh_token,
            'expires_in': expires_in,
            'scope': auth_obj.scope
        }

        self.client = soundcloud.Client(access_token=auth_obj.access_token)
        user_obj = self.client.get('/me')

        user_data = {
            'id': user_obj.id,
            'country': user_obj.country,
            'username': user_obj.username,
            'profile_url': user_obj.permalink_url,
            'avatar_url': user_obj.avatar_url
        }

        response = {
            'auth': auth_data,
            'user': user_data
        }

        return response

    def lookup_track(self, track_id):
        """Lookup a single track using the soundcloud API
        """
        logger.info('Track lookup: {0}'.format(track_id))

        try:
            track = self.client.get('/tracks', ids=track_id)[0].obj
        except IndexError:
            raise TrackNotFound('Soundcloud: {0}'.format(track_id))
        return _transform_track(track)

    def search_tracks(self, query, limit=200, offset=0):
        """Search for tracks using the soundcloud API
        """
        logger.info('Searching: Limit {0}, Offset {1}'.format(limit, offset))

        tracks = self.client.get(
            '/tracks', q=query, limit=limit, offset=offset)

        return [_transform_track(x.obj) for x in tracks]

    def playlists(self, user_id, token):
        """Lookup user playlists using the Spotify Web API

        Returns standard radiobabel playlist list response.
        """
        try:
            playlists = self.client.get('/me/playlists')
        except:
            raise PlaylistNotFound('Soundcloud: {0}'.format(user_id))

        logger.info('Playlist lookup: {0}'.format(user_id))

        transform_playlists = []
        for playlist in playlists:
            transformed_playlist = _transform_playlist(playlist)
            transform_playlists.append(transformed_playlist)

        return transform_playlists

    def playlist_tracks(self, playlist_id, user_id, token, limit=20, offset=0):
        """Search for tracks using the soundcloud API
        """
        logger.info('Searching: Limit {0}, Offset {1}'.format(limit, offset))

        url = '/me/playlists/{0}'.format(playlist_id)
        try:
            playlist_tracks = self.client.get(url, limit=limit, offset=offset)
        except:
            raise PlaylistNotFound('Soundcloud: {0}'.format(playlist_id))

        return [_transform_track(x) for x in playlist_tracks.tracks]

    def favorites(self, user_id, token, limit=20, offset=0):
        """Lookup user favourite tracks using the soundcloud Web API.

        Returns standard radiobabel track list response.
        """
        logger.info('Searching: Limit {0}, Offset {1}'.format(limit, offset))

        url = '/users/{0}/favorites'.format(user_id)
        try:
            fav_tracks = self.client.get(url, limit=limit, offset=offset)
        except:
            raise PlaylistNotFound('Soundcloud: {0}'.format(user_id))

        return [_transform_track(x.obj) for x in fav_tracks]
