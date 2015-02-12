# stdlib imports
import os

# third-party imports
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient


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
