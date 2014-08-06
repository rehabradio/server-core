import json
from django.test import TestCase


class BaseTestCase(TestCase):
    """
    Load in default data for tests
    """
    fixtures = ['radio/fixtures/testdata.json']


class MetadataAPIRootViewTestCase(BaseTestCase):
    """
    Root index for all metadata routes
    List of endpoint links for further navigation
    """
    def test_get(self):
        resp = self.client.get('/api/metadata/')
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
    List of endpoint links for track lookups, example urls provided under "tracks"
    """
    def test_get(self):
        resp = self.client.get('/api/metadata/lookup/')
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
        track_attrs = (
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
        )

        resp1 = self.client.get('/api/metadata/lookup/spotify/6MeNtkNT4ENE5yohNvGqd4/')
        data1 = json.loads(resp1.content)

        # Ensure request was successful
        self.assertEqual(resp1.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(track_attrs) <= set(data1))

        resp2 = self.client.get('/api/metadata/lookup/soundcloud/153868082/')
        data2 = json.loads(resp2.content)

        # Ensure request was successful
        self.assertEqual(resp2.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(track_attrs) <= set(data2))

    """
    Test 404 error and detail message returns, using a bad backend
    """
    def test_get_bad_backend(self):
        resp = self.client.get('/api/metadata/lookup/test/153868082/')
        data = json.loads(resp.content)

        # Ensure request failed
        self.assertEqual(resp.status_code, 404)
        # Ensure "detail" message is set, and the message matches expected
        self.assertEqual(data['detail'], 'Invalid backend, provider not recognised.')



class SearchRootViewTestCase(BaseTestCase):
    """
    Root index for all metadata/search routes
    List of endpoint links for search lookups, example urls provided under "tracks"
    """
    def test_get(self):
        resp = self.client.get('/api/metadata/search/')
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
        track_attrs = (
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
        )

        resp1 = self.client.get('/api/metadata/search/spotify/?q=Haim/')
        data1 = json.loads(resp1.content)
        tracks1 = data1['results'][0]

        # Ensure request was successful
        self.assertEqual(resp1.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(result_attrs) <= set(data1))
        self.assertTrue(set(track_attrs) <= set(tracks1))

        resp2 = self.client.get('/api/metadata/search/soundcloud/?q=narsti/')
        data2 = json.loads(resp2.content)
        tracks2 = data2['results'][0]

        # Ensure request was successful
        self.assertEqual(resp2.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(result_attrs) <= set(data2))
        self.assertTrue(set(track_attrs) <= set(tracks2))

    """
    Test 404 error and detail message returns, using a bad backend
    """
    def test_get_bad_backend(self):
        resp = self.client.get('/api/metadata/search/test/?q=Haim/')
        data = json.loads(resp.content)

        # Ensure request failed
        self.assertEqual(resp.status_code, 404)
        # Ensure "detail" message is set, and the message matches expected
        self.assertEqual(data['detail'], 'Invalid backend, provider not recognised.')

    """
    Test 400 error and detail message returns, if no "q" parameter is set
    """
    def test_get_no_parameter(self):
        resp = self.client.get('/api/metadata/search/soundcloud/')
        data = json.loads(resp.content)

        # Ensure request failed
        self.assertEqual(resp.status_code, 400)
        # Ensure "detail" message is set, and the message matches expected
        self.assertEqual(data['detail'], 'Required parameters are missing')
