import json
import os

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient

from .models import Track


class BaseTestCase(TestCase):
    """
    Load in default data for tests
    """
    fixtures = ['radio/fixtures/testdata.json']
    factory = APIRequestFactory()
    api_client = APIClient()


class MetadataAPIRootViewTestCase(BaseTestCase):
    """
    Root index for all metadata routes
    List of endpoint links for further navigation
    """
    def test_get(self):
        resp = self.api_client.get('/api/metadata/')
        data = json.loads(resp.content)

        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(data['endpoints'])
        self.assertTrue(data['endpoints']['search'])
        self.assertTrue(data['endpoints']['lookup'])


class LookupRootViewTestCase(BaseTestCase):
    """
    Root index for all metadata/lookup routes
    List of endpoint links for track lookups
    """
    def test_get(self):
        resp = self.api_client.get('/api/metadata/lookup/')
        data = json.loads(resp.content)

        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(data['endpoints'])
        self.assertTrue(data['endpoints']['soundcloud'])
        self.assertTrue(data['endpoints']['soundcloud']['tracks'])
        self.assertTrue(data['endpoints']['spotify'])
        self.assertTrue(data['endpoints']['spotify']['tracks'])


class LookupViewTestCase(BaseTestCase):
    """
    Test looking up a track using the spotify and soundcloud backends
    """
    def test_get(self):
        expected_attrs = (
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

        resp1 = self.api_client.get(
            '/api/metadata/lookup/spotify/6MeNtkNT4ENE5yohNvGqd4/'
        )
        data1 = json.loads(resp1.content)

        # Ensure request was successful
        self.assertEqual(resp1.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(expected_attrs) <= set(data1))

        resp2 = self.api_client.get(
            '/api/metadata/lookup/soundcloud/153868082/'
        )
        data2 = json.loads(resp2.content)

        # Ensure request was successful
        self.assertEqual(resp2.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(expected_attrs) <= set(data2))

    """
    Test 404 error and detail message returns, using a bad backend
    """
    def test_get_bad_backend(self):
        resp = self.api_client.get('/api/metadata/lookup/test/153868082/')
        data = json.loads(resp.content)

        # Ensure request failed
        self.assertEqual(resp.status_code, 404)
        # Ensure "detail" message is set, and the message matches expected
        self.assertEqual(
            data['detail'],
            'Invalid backend, provider not recognised.'
        )


class SearchRootViewTestCase(BaseTestCase):
    """
    Root index for all metadata/search routes
    List of endpoint links for search lookups
    """
    def test_get(self):
        resp = self.api_client.get('/api/metadata/search/')
        data = json.loads(resp.content)

        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(data['endpoints'])
        self.assertTrue(data['endpoints']['soundcloud'])
        self.assertTrue(data['endpoints']['soundcloud']['tracks'])
        self.assertTrue(data['endpoints']['spotify'])
        self.assertTrue(data['endpoints']['spotify']['tracks'])


class SearchViewTestCase(BaseTestCase):
    """
    Test searching for tracks using the spotify and soundcloud backends
    """
    def test_get(self):
        result_attrs = (
            'count',
            'next',
            'previous',
            'results',
        )
        expected_results_attrs = (
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

        resp1 = self.api_client.get('/api/metadata/search/spotify/?q=Haim/')
        data1 = json.loads(resp1.content)
        tracks1 = data1['results'][0]

        # Ensure request was successful
        self.assertEqual(resp1.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(result_attrs) <= set(data1))
        self.assertTrue(set(expected_results_attrs) <= set(tracks1))

        resp2 = self.api_client.get(
            '/api/metadata/search/soundcloud/?q=narsti/'
        )
        data2 = json.loads(resp2.content)
        tracks2 = data2['results'][0]

        # Ensure request was successful
        self.assertEqual(resp2.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(result_attrs) <= set(data2))
        self.assertTrue(set(expected_results_attrs) <= set(tracks2))

    """
    Test 404 error and detail message returns, using a bad backend
    """
    def test_get_bad_backend(self):
        resp = self.api_client.get('/api/metadata/search/test/?q=Haim/')
        data = json.loads(resp.content)

        # Ensure request failed
        self.assertEqual(resp.status_code, 404)
        # Ensure "detail" message is set, and the message matches expected
        self.assertEqual(
            data['detail'],
            'Invalid backend, provider not recognised.'
        )

    """
    Test 400 error and detail message returns, if no "q" parameter is set
    """
    def test_get_no_parameter(self):
        resp = self.api_client.get('/api/metadata/search/soundcloud/')
        data = json.loads(resp.content)

        # Ensure request failed
        self.assertEqual(resp.status_code, 400)
        # Ensure "detail" message is set, and the message matches expected
        self.assertEqual(data['detail'], 'Required parameters are missing')


class TrackViewSetTestCase(TestCase):
    """
    Load in default data for tests
    """
    fixtures = ['radio/fixtures/testdata.json']
    factory = APIRequestFactory()
    api_client = APIClient()

    """
    Log in a user
    """
    def setUp(self):
        username = os.environ.get('TEST_USERNAME', None)
        password = os.environ.get('TEST_PASSWORD', None)
        login = self.api_client.login(username=username, password=password)
        self.assertEqual(login, True)

    """
    Retrieve a list of all Tracks, with an excepted result set
    """
    def test_list(self):
        expected_attrs = (
            'count',
            'next',
            'previous',
            'results',
        )

        expected_results_attrs = (
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

        resp = self.api_client.get('/api/metadata/tracks/')
        data = json.loads(resp.content)
        Tracks = data['results'][0]

        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(expected_attrs) <= set(data))
        self.assertTrue(set(expected_results_attrs) <= set(Tracks))

    """
    Create a Track with all data
    """
    def test_create(self):
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

    """
    Create a track with no source id
    """
    def test_create_with_no_source_id(self):
        # Count the number of records before the save
        existing_records_count = Track.objects.all().count()
        post_data = {
            'source_type': 'spotify',
        }

        resp = self.api_client.post('/api/metadata/tracks/', data=post_data)
        data = json.loads(resp.content)
        new_records_count = Track.objects.all().count()

        # Ensure request failed
        self.assertEqual(resp.status_code, 400)
        # Ensure a new record was not added to the database
        self.assertEqual(existing_records_count, new_records_count)
        # Ensure validation flags where raised for each field
        self.assertEqual(data['detail'], 'Track could not be found')

    """
    Create a track with bad backend
    """
    def test_create_with_bad_backend(self):
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
        self.assertEqual(resp.status_code, 400)
        # Ensure a new record was not added to the database
        self.assertEqual(existing_records_count, new_records_count)
        # Ensure validation flags where raised for each field
        self.assertEqual(data['detail'], 'Track could not be found')

    """
    Retrieve a track
    """
    def test_retrieve(self):
        expected_attrs = (
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

        resp = self.api_client.get('/api/metadata/tracks/1/')
        data = json.loads(resp.content)

        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(expected_attrs) <= set(data))

    """
    Cascade remove a track from the database
    """
    def test_destroy(self):
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
