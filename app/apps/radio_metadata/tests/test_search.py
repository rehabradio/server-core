# stdlib imports
import json

# third-party imports
from django.core.cache import cache

# local imports
from .test_base import BaseTestCase
from radio.utils.cache import build_key


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
    def test_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get('/api/metadata/search/')
        self.assertEqual(resp.status_code, 403)

    def test_get_spotify(self):
        """Return a json object for spotify backend."""
        resp = self.api_client.get('/api/metadata/search/spotify/?q=Haim')
        data = json.loads(resp.content)
        tracks = data['results'][0]
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.paginated_attrs) <= set(data))
        self.assertTrue(set(self.track_attrs) <= set(tracks))

    def test_get_soundcloud(self):
        """Return a json object for soundcloud backend."""
        resp = self.api_client.get('/api/metadata/search/soundcloud/?q=Haim')
        data = json.loads(resp.content)
        tracks = data['results'][0]
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.paginated_attrs) <= set(data))
        self.assertTrue(set(self.track_attrs) <= set(tracks))

    def test_get_youtube(self):
        """Return a json object for youtube backend."""
        resp = self.api_client.get(
            '/api/metadata/search/youtube/?q=everything%20is%20awesome')
        data = json.loads(resp.content)
        tracks = data['results'][0]
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.paginated_attrs) <= set(data))
        self.assertTrue(set(self.track_attrs) <= set(tracks))

    def test_get_cached(self):
        self.api_client.get('/api/metadata/search/youtube/?q=Haim')
        resp = self.api_client.get('/api/metadata/search/youtube/?q=Haim')
        return_data = json.loads(resp.content)

        cache_key = build_key('mtdttrcksrch', 'youtube', 'Haim', '1')
        cached_data = cache.get(cache_key)

        self.assertEqual(return_data, cached_data)

    def test_get_bad_backend(self):
        """Throw a 404 response error with a detail message."""
        resp = self.api_client.get('/api/metadata/search/test/?q=Haim')
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
