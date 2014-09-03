# stdlib imports
import json
import os
# third-party imports
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
# local imports
from .models import Track


class BaseTestCase(TestCase):
    """Load in default data for tests, and login user."""
    fixtures = ['radio/fixtures/testdata.json']
    factory = APIRequestFactory()
    api_client = APIClient()
    paginated_attrs = ('count', 'next', 'previous', 'results')
    track_attrs = (
        'source_type',
        'source_id',
        'name',
        'artists',
        'album',
        'duration_ms',
        'preview_url',
        'uri',
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
        """Ensure Auth is required and log in the test user."""
        username = os.environ.get('TEST_USERNAME', None)
        password = os.environ.get('TEST_PASSWORD', None)

        login = self.api_client.login(username=username, password=password)
        self.assertEqual(login, True)


class MetadataAPIRootViewTestCase(BaseTestCase):
    """Root index for all metadata routes."""
    def test_get(self):
        """Return a valid response."""
        resp = self.api_client.get('/api/metadata/')
        self.assertEqual(resp.status_code, 200)


class LookupRootViewTestCase(BaseTestCase):
    """Root index for all metadata/lookup routes."""
    def test_get(self):
        """Return a valid response."""
        resp = self.api_client.get('/api/metadata/lookup/')
        self.assertEqual(resp.status_code, 200)


class LookupViewTestCase(BaseTestCase):
    """Uses a backend(spotify/soundcloud) and a source ID,
    fetch a track from the given backend api.
    """
    def test_spotify_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get(
            '/api/metadata/lookup/spotify/6MeNtkNT4ENE5yohNvGqd4/'
        )
        self.assertEqual(resp.status_code, 403)

    def test_soundcloud_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get(
            '/api/metadata/lookup/soundcloud/153868082/'
        )
        self.assertEqual(resp.status_code, 403)

    def test_get_spotify(self):
        """Return a json object for spotify backend."""
        resp = self.api_client.get(
            '/api/metadata/lookup/spotify/6MeNtkNT4ENE5yohNvGqd4/'
        )
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.track_attrs) <= set(data))

    def test_get_soundcloud(self):
        """Return a json object for soundcloud backend."""
        resp = self.api_client.get(
            '/api/metadata/lookup/soundcloud/153868082/'
        )
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.track_attrs) <= set(data))

    def test_get_with_bad_backend(self):
        """Throw a 404 response error with a detail message."""
        resp = self.api_client.get('/api/metadata/lookup/test/153868082/')
        data = json.loads(resp.content)
        # Ensure request failed
        self.assertEqual(resp.status_code, 404)
        # Ensure "detail" message is set, and the message matches expected
        self.assertEqual(
            data['detail'],
            u'Invalid backend, provider not recognised.'
        )

    def test_get_with_bad_souce_id(self):
        """Throw a 404 response error with a detail message."""
        resp = self.api_client.get('/api/metadata/lookup/soundcloud/1/')
        data = json.loads(resp.content)
        # Ensure request failed
        self.assertEqual(resp.status_code, 404)
        # Ensure "detail" message is set, and the message matches expected
        self.assertEqual(data['detail'], u'The record could not be found.')


class SearchRootViewTestCase(BaseTestCase):
    """Root index for all metadata/search routes."""
    def test_get(self):
        """Return a valid response."""
        resp = self.api_client.get('/api/metadata/search/')
        self.assertEqual(resp.status_code, 200)


class SearchViewTestCase(BaseTestCase):
    """Uses a backend(spotify/soundcloud) and a `q` parament,
    to search for tracks from the given backend api.
    """
    def test_spotify_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get(
            '/api/metadata/search/spotify/?q=Haim/'
        )
        self.assertEqual(resp.status_code, 403)

    def test_soundcloud_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get(
            '/api/metadata/search/soundcloud/?q=Haim/'
        )
        self.assertEqual(resp.status_code, 403)

    def test_get_spotify(self):
        """Return a json object for spotify backend."""
        resp = self.api_client.get('/api/metadata/search/spotify/?q=Haim/')
        data = json.loads(resp.content)
        tracks = data['results'][0]
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.paginated_attrs) <= set(data))
        self.assertTrue(set(self.track_attrs) <= set(tracks))

    def test_get_soundcloud(self):
        """Return a json object for soundcloud backend."""
        resp = self.api_client.get('/api/metadata/search/soundcloud/?q=Haim/')
        data = json.loads(resp.content)
        tracks = data['results'][0]
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.paginated_attrs) <= set(data))
        self.assertTrue(set(self.track_attrs) <= set(tracks))

    def test_get_bad_backend(self):
        """Throw a 404 response error with a detail message."""
        resp = self.api_client.get('/api/metadata/search/test/?q=Haim/')
        data = json.loads(resp.content)
        # Ensure request failed
        self.assertEqual(resp.status_code, 404)
        # Ensure "detail" message is set, and the message matches expected
        self.assertEqual(
            data['detail'],
            u'Invalid backend, provider not recognised.'
        )

    def test_get_no_parameter(self):
        """Throw a 404 response error with a detail message."""
        resp = self.api_client.get('/api/metadata/search/soundcloud/')
        data = json.loads(resp.content)
        # Ensure request failed
        self.assertEqual(resp.status_code, 400)
        # Ensure "detail" message is set, and the message matches expected
        self.assertEqual(data['detail'], u'Required parameters are missing.')


class UserRootViewTestCase(BaseTestCase):
    """Root index for all metadata/search routes."""
    def test_get(self):
        """Return a valid response."""
        resp = self.api_client.get('/api/metadata/user/')
        self.assertEqual(resp.status_code, 200)


class UserPlaylistViewSetTestCase(BaseTestCase):
    """Uses a backend(spotify/soundcloud) and a `q` parament,
    to search for tracks from the given backend api.
    """
    def test_list_soundcloud_with_no_oauth(self):
        """Return a list of playlist json objects."""
        resp = self.api_client.get('/api/metadata/user/playlists/soundcloud/')
        self.assertEqual(resp.status_code, 403)

    def test_list_spotify_with_no_oauth(self):
        """Return a list of playlist json objects."""
        resp = self.api_client.get('/api/metadata/user/playlists/spotify/')
        self.assertEqual(resp.status_code, 403)


class TrackViewSetTestCase(BaseTestCase):
    """CRUD commands for the track database table."""
    def test_list_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get('/api/metadata/tracks/')
        self.assertEqual(resp.status_code, 403)

    def test_detail_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get('/api/metadata/tracks/1/')
        self.assertEqual(resp.status_code, 403)

    def test_list(self):
        """Return a paginated set of track json objects."""
        track_attrs = self.track_attrs + ('id',)
        resp = self.api_client.get('/api/metadata/tracks/')
        data = json.loads(resp.content)
        tracks = data['results'][0]
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.paginated_attrs) <= set(data))
        self.assertTrue(set(track_attrs) <= set(tracks))

    def test_create(self):
        """Add a track to the database.
        Returns a track json object of the newly created record.
        """
        # Count the number of records before the save
        existing_records_count = Track.objects.all().count()
        post_data = {
            'source_type': 'spotify',
            'source_id': '4bCOAuhvjsxbVBM5MM8oik',
        }

        resp = self.api_client.post('/api/metadata/tracks/', data=post_data)
        new_records_count = Track.objects.all().count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure a new record was created in the database
        self.assertEqual(existing_records_count+1, new_records_count)

    def test_create_with_bad_id(self):
        """Try to create a track, with a bad source_id.
        Returns a 404 response with detail message.
        """
        # Count the number of records before the save
        existing_records_count = Track.objects.all().count()
        post_data = {'source_type': 'spotify', 'source_id': 0}
        resp = self.api_client.post('/api/metadata/tracks/', data=post_data)
        data = json.loads(resp.content)
        new_records_count = Track.objects.all().count()
        # Ensure request failed
        self.assertEqual(resp.status_code, 404)
        # Ensure a new record was not added to the database
        self.assertEqual(existing_records_count, new_records_count)
        # Ensure validation flags where raised for each field
        self.assertEqual(data['detail'], u'The record could not be found.')

    def test_create_with_bad_backend(self):
        """Returns a 404 response with detail message."""
        # Count the number of records before the save
        existing_records_count = Track.objects.all().count()
        post_data = {
            'source_type': 'test',
            'source_id': '4bCOAuhvjsxbVBM5MM8oik',
        }
        resp = self.api_client.post('/api/metadata/tracks/', data=post_data)
        data = json.loads(resp.content)
        new_records_count = Track.objects.all().count()
        # Ensure request failed
        self.assertEqual(resp.status_code, 404)
        # Ensure a new record was not added to the database
        self.assertEqual(existing_records_count, new_records_count)
        # Ensure validation flags where raised for each field
        self.assertEqual(data['detail'], u'The record could not be found.')

    def test_retrieve(self):
        """Return a track json object of a given record."""
        track_attrs = self.track_attrs + ('id',)
        resp = self.api_client.get('/api/metadata/tracks/1/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(track_attrs) <= set(data))

    def test_retrieve_with_bad_id(self):
        """Returns a 404 response with detail message."""
        resp = self.api_client.get('/api/metadata/tracks/100000/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 404)
        # Ensure the returned json keys match the expected
        self.assertEqual(data['detail'], u'Not found')

    def test_destroy(self):
        """Remove a track from the database
        Returns a successful response, with a detail message.
        """
        # Count the number of records before the save
        existing_records_count = Track.objects.all().count()
        resp = self.api_client.delete('/api/metadata/tracks/2/')
        data = json.loads(resp.content)
        new_records_count = Track.objects.all().count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the record was removed from the database
        self.assertEqual(existing_records_count-1, new_records_count)
        # Ensure "detail" message is set, and the message matches expected
        self.assertEqual(data['detail'], 'Track successfully removed')

    def test_delete_with_bad_id(self):
        """Returns a 404 response with detail message."""
        resp = self.api_client.delete('/api/metadata/tracks/100000/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 404)
        # Ensure the returned json keys match the expected
        self.assertEqual(data['detail'], u'The record could not be found.')
