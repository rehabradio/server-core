# stdlib imports
import json

# third-party imports
from django.core.cache import cache

# local imports
from .test_base import BaseTestCase
from radio.utils.cache import build_key


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
    def test_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get('/api/metadata/lookup/')
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

    def test_get_youtube(self):
        """Return a json object for youtube backend."""
        resp = self.api_client.get(
            '/api/metadata/lookup/youtube/StTqXEQ2l-Y/'
        )
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.track_attrs) <= set(data))

    def test_get_cached(self):
        self.api_client.get('/api/metadata/lookup/soundcloud/153868082/')
        resp = self.api_client.get(
            '/api/metadata/lookup/soundcloud/153868082/'
        )
        return_data = json.loads(resp.content)

        cache_key = build_key('mtdt-lkp', 'soundcloud', 153868082)
        cached_data = cache.get(cache_key)

        self.assertEqual(return_data, cached_data)

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
