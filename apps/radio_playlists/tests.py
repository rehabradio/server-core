# stdlib imports
import json
import os
# third-party imports
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
# local imports
from .models import Playlist, PlaylistTrack
from radio_metadata.models import Track


class BaseTestCase(TestCase):
    """Load in default data for tests, and login user."""
    fixtures = ['radio/fixtures/testdata.json']
    factory = APIRequestFactory()
    api_client = APIClient()
    paginated_attrs = ('count', 'next', 'previous', 'results')
    playlist_attrs = ('id', 'name', 'description', 'created', 'updated')
    playlist_track_attrs = ('id', 'track', 'position', 'owner')
    track_attrs = (
        'id',
        'source_type',
        'source_id',
        'name',
        'artists',
        'album',
        'duration_ms',
        'preview_url',
        'track_number',
        'image_small',
        'image_medium',
        'image_large',
        'play_count',
        'owner',
        'created',
        'updated',
    )

    def setUp(self):
        """Log in the test user."""
        username = os.environ.get('TEST_USERNAME', None)
        password = os.environ.get('TEST_PASSWORD', None)
        login = self.api_client.login(username=username, password=password)
        self.assertEqual(login, True)


class PlaylistViewSetTestCase(BaseTestCase):
    """CRUD commands for the playlist database table"""
    def test_list(self):
        """Return a paginated set of playlist json objects."""
        resp = self.api_client.get('/api/playlists/')
        data = json.loads(resp.content)
        playlists = data['results'][0]
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.paginated_attrs) <= set(data))
        self.assertTrue(set(self.playlist_attrs) <= set(playlists))

    def test_create(self):
        """Add a playlist to the database.
        Returns a playlist json object of the newly created record.
        """
        # Count the number of records before the save
        existing_records_count = Playlist.objects.all().count()
        post_data = {
            'name': 'test playlist',
            'description': 'a playlist for tdd',
        }

        resp = self.api_client.post('/api/playlists/', data=post_data)
        data = json.loads(resp.content)
        new_records_count = Playlist.objects.all().count()

        # Ensure request was successful
        self.assertEqual(resp.status_code, 201)
        # Ensure a new record was created in the database
        self.assertEqual(existing_records_count+1, new_records_count)
        # Ensure the returned json keys match the expected
        self.assertRegexpMatches(str(data['id']), r'[0-9]+')
        self.assertEqual(data['name'], post_data['name'])
        self.assertEqual(data['description'], post_data['description'])
        self.assertTrue(set(self.playlist_attrs) <= set(data))

    def test_create_with_empty_values(self):
        """Try to create a track, with a empty post data.
        Returns a 404 response with detail message.
        """
        # Count the number of records before the save
        existing_records_count = Playlist.objects.all().count()
        post_data = {
            'name': '',
            'description': '',
        }

        resp = self.api_client.post('/api/playlists/', data=post_data)
        data = json.loads(resp.content)
        new_records_count = Playlist.objects.all().count()
        # Ensure request failed
        self.assertEqual(resp.status_code, 400)
        # Ensure a new record was not added to the database
        self.assertEqual(existing_records_count, new_records_count)
        # Ensure validation flags where raised for each field
        self.assertEqual(data['name'], ['This field is required.'])
        self.assertEqual(data['description'], ['This field is required.'])

    def test_retrieve(self):
        """Return a playlist json object of a given record."""
        resp = self.api_client.get('/api/playlists/1/')
        data = json.loads(resp.content)

        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.playlist_attrs) <= set(data))

    def test_retrieve_with_bad_id(self):
        """Returns a 404 response with detail message."""
        resp = self.api_client.get('/api/playlists/100000/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 404)
        # Ensure the returned json keys match the expected
        self.assertEqual(data['detail'], u'Not found')

    def test_update(self):
        """Update a playlist from the database.
        Returns a playlist json object of the updated record.
        """
        # Count the number of records before the save
        existing_records_count = Playlist.objects.all().count()
        post_data = {
            'name': 'updated playlist',
            'description': 'playlist is now updated',
        }

        resp = self.api_client.put('/api/playlists/1/', data=post_data)
        new_record = Playlist.objects.filter(id=1).values()[0]
        new_records_count = Playlist.objects.all().count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure a the record was updated
        # and a new records was not added to the database
        self.assertEqual(existing_records_count, new_records_count)
        self.assertEqual(new_record['name'], post_data['name'])
        self.assertEqual(new_record['description'], post_data['description'])

    def test_partial_update(self):
        """Update a single piece of playlist information from the database.
        Returns a playlist json object of the updated record.
        """
        # Count the number of records before the save
        existing_records_count = Playlist.objects.all().count()
        post_data = {'name': 'patched playlist'}

        resp = self.api_client.patch('/api/playlists/1/', data=post_data)
        new_record = Playlist.objects.filter(id=1).values()[0]
        new_records_count = Playlist.objects.all().count()

        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure a the record was updated
        # and a new records was not added to the database
        self.assertEqual(existing_records_count, new_records_count)
        self.assertEqual(new_record['name'], post_data['name'])

    def test_destroy(self):
        """Recursively remove a playlist and its associated playlist
        tracks from the database

        Returns a successful response, with a detail message.
        """
        # Count the number of records before the save
        existing_records_count = Playlist.objects.all().count()

        resp = self.api_client.delete('/api/playlists/2/')
        data = json.loads(resp.content)
        new_records_count = Playlist.objects.all().count()

        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the record was removed from the database
        self.assertEqual(existing_records_count-1, new_records_count)
        # Ensure "detail" message is set, and the message matches expected
        self.assertEqual(data['detail'], 'playlist successfully removed')

    def test_delete_with_bad_id(self):
        """Returns a 404 response with detail message."""
        resp = self.api_client.delete('/api/playlists/100000/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 404)
        # Ensure the returned json keys match the expected
        self.assertEqual(data['detail'], u'The record could not be found.')


class PlaylistTrackViewSetTestCase(BaseTestCase):
    """CRUD commands for the playlist_track database table."""
    def test_list(self):
        """Return a paginated set of playlist track json objects."""
        resp = self.api_client.get('/api/playlists/1/tracks/')
        data = json.loads(resp.content)
        playlist_tracks = data['results'][0]
        track = playlist_tracks['track']
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.paginated_attrs) <= set(data))
        self.assertTrue(set(self.playlist_track_attrs) <= set(playlist_tracks))
        self.assertTrue(set(self.track_attrs) <= set(track))

    def test_create(self):
        """Add a playlist track to the database.
        params - track

        Returns a playlist track json object of the newly created record.
        """
        # Count the number of records before the save
        existing_records_count = PlaylistTrack.objects.filter(
            playlist=2
        ).count()
        track = Track.objects.get(id=3)
        post_data = {
            'track': track.id,
        }

        resp = self.api_client.post('/api/playlists/2/tracks/', data=post_data)
        data = json.loads(resp.content)
        new_records_count = PlaylistTrack.objects.filter(playlist=2).count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure a new record was created in the database
        self.assertEqual(existing_records_count+1, new_records_count)
        # Ensure the returned json keys match the expected
        self.assertRegexpMatches(str(data['id']), r'[0-9]+')
        self.assertEqual(data['track']['id'], track.id)
        self.assertEqual(data['position'], int(new_records_count))

    def test_create_with_empty_values(self):
        """Try to create a track, empty post variables.
        Returns a 404 response with detail message.
        """
        # Count the number of records before the save
        existing_records_count = PlaylistTrack.objects.filter(
            playlist=1
        ).count()
        post_data = {
            'track': None,
        }

        resp = self.api_client.post('/api/playlists/2/tracks/', data=post_data)
        data = json.loads(resp.content)
        new_records_count = PlaylistTrack.objects.filter(playlist=1).count()

        # Ensure request failed
        self.assertEqual(resp.status_code, 400)
        # Ensure a new record was not added to the database
        self.assertEqual(existing_records_count, new_records_count)
        # Ensure validation flags where raised for each field
        self.assertEqual(data['detail'], u'The record could not be saved.')

    def test_retrieve(self):
        """Return a track json object of a given record."""
        resp = self.api_client.get('/api/playlists/1/tracks/3/')
        data = json.loads(resp.content)
        track = data['track']
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.playlist_track_attrs) <= set(data))
        self.assertTrue(set(self.track_attrs) <= set(track))

    def test_retrieve_with_bad_id(self):
        """Returns a 404 response with detail message."""
        resp = self.api_client.get('/api/playlists/1/tracks/100000/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 404)
        # Ensure the returned json keys match the expected
        self.assertEqual(data['detail'], u'Not found')

    def test_partial_update(self):
        """Update a playlist track's position.
        Returns a playlist track json object of the updated record.
        """
        # Count the number of records before the save
        existing_records_count = PlaylistTrack.objects.filter(
            playlist=1
        ).count()
        post_data = {'position': 33}

        resp = self.api_client.patch(
            '/api/playlists/1/tracks/3/',
            data=post_data
        )
        data = json.loads(resp.content)
        new_records_count = PlaylistTrack.objects.filter(playlist=1).count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure a new record was created in the database
        self.assertEqual(existing_records_count, new_records_count)
        # Ensure the returned json keys match the expected
        self.assertEqual(int(data['position']), post_data['position'])

    def test_destroy(self):
        """Remove a playlist track from the database
        Returns a successful response, with a detail message.
        """
        # Count the number of records before the save
        existing_records_count = PlaylistTrack.objects.filter(
            playlist=1
        ).count()

        resp = self.api_client.delete('/api/playlists/1/tracks/3/')
        data = json.loads(resp.content)
        new_records_count = PlaylistTrack.objects.filter(playlist=1).count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the record was removed from the database
        self.assertEqual(existing_records_count-1, new_records_count)
        # Ensure "detail" message is set, and the message matches expected
        self.assertEqual(data['detail'], 'Track removed from playlist')

    def test_delete_with_bad_id(self):
        """Returns a 404 response with detail message."""
        resp = self.api_client.delete('/api/playlists/1/tracks/100000/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 404)
        # Ensure the returned json keys match the expected
        self.assertEqual(data['detail'], u'The record could not be found.')
