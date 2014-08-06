import json
from django.test import TestCase


class BaseTestCase(TestCase):
    fixtures = ['radio/fixtures/testdata.json']


class MetadataAPIRootViewTestCase(BaseTestCase):
    def test_get(self):
        resp = self.client.get('/api/metadata/')
        data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data['endpoints'])
        self.assertTrue(data['endpoints']['search'])
        self.assertTrue(data['endpoints']['lookup'])

class LookupRootViewTestCase(BaseTestCase):
    def test_get(self):
        resp = self.client.get('/api/metadata/lookup/')
        data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data['endpoints'])
        self.assertTrue(data['endpoints']['soundcloud'])
        self.assertTrue(data['endpoints']['soundcloud']['tracks'])
        self.assertTrue(data['endpoints']['spotify'])
        self.assertTrue(data['endpoints']['spotify']['tracks'])


class LookupViewTestCase(BaseTestCase):
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

        self.assertEqual(resp1.status_code, 200)
        self.assertTrue(set(track_attrs) <= set(data1))

        resp2 = self.client.get('/api/metadata/lookup/soundcloud/153868082/')
        data2 = json.loads(resp2.content)

        self.assertEqual(resp2.status_code, 200)
        self.assertTrue(set(track_attrs) <= set(data2))

    def test_get_bad_backend(self):
        resp = self.client.get('/api/metadata/lookup/test/153868082/')
        data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['detail'], 'Invalid backend, provider not recognised.')



class SearchRootViewTestCase(BaseTestCase):
    def test_get(self):
        resp = self.client.get('/api/metadata/search/')
        data = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)

        self.assertTrue(data['endpoints'])
        self.assertTrue(data['endpoints']['soundcloud'])
        self.assertTrue(data['endpoints']['soundcloud']['tracks'])
        self.assertTrue(data['endpoints']['spotify'])
        self.assertTrue(data['endpoints']['spotify']['tracks'])


class SearchViewTestCase(BaseTestCase):
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

        self.assertEqual(resp1.status_code, 200)
        self.assertTrue(set(result_attrs) <= set(data1))
        self.assertTrue(set(track_attrs) <= set(tracks1))

        resp2 = self.client.get('/api/metadata/search/soundcloud/?q=narsti/')
        data2 = json.loads(resp2.content)
        tracks2 = data2['results'][0]

        self.assertEqual(resp2.status_code, 200)
        self.assertTrue(set(result_attrs) <= set(data2))
        self.assertTrue(set(track_attrs) <= set(tracks2))

    def test_get_bad_backend(self):
        resp = self.client.get('/api/metadata/search/test/?q=Haim/')
        data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['detail'], 'Invalid backend, provider not recognised.')

    def test_get_no_parameter(self):
        resp = self.client.get('/api/metadata/search/soundcloud/')
        data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['detail'], 'Required parameters are missing')
