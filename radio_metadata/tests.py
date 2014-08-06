from django.test import TestCase


class BaseTestCase(TestCase):
    fixtures = ['radio/fixtures/testdata.json']


class MetadataAPIRootViewTestCase(BaseTestCase):
    def test_get(self):
        resp = self.client.get('/api/metadata/')
        self.assertEqual(resp.status_code, 200)


class LookupRootViewTestCase(BaseTestCase):
    def test_get(self):
        resp = self.client.get('/api/metadata/lookup/')
        self.assertEqual(resp.status_code, 200)


class LookupViewTestCase(BaseTestCase):
    def test_get(self):
        resp = self.client.get('/api/metadata/lookup/spotify/6MeNtkNT4ENE5yohNvGqd4/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/api/metadata/lookup/soundcloud/153868082/')
        self.assertEqual(resp.status_code, 200)


class SearchRootViewTestCase(BaseTestCase):
    def test_get(self):
        resp = self.client.get('/api/metadata/search/')
        self.assertEqual(resp.status_code, 200)


class SearchViewTestCase(BaseTestCase):
    def test_get(self):
        resp = self.client.get('/api/metadata/search/spotify/?q=Haim/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/api/metadata/search/soundcloud/?q=narsti/')
        self.assertEqual(resp.status_code, 200)
