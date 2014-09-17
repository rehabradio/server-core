# stdlib imports
import json
import os

# third-party imports
from django.test import TestCase
from rest_framework.test import APIClient


class BaseTestCase(TestCase):
    """Load in default data for tests, and login user."""
    fixtures = ['radio/fixtures/testdata.json']
    api_client = APIClient()

    def setUp(self):
        """Ensure Auth is required and log in the test user."""
        username = os.environ.get('TEST_USERNAME', None)
        password = os.environ.get('TEST_PASSWORD', None)

        login = self.api_client.login(username=username, password=password)
        self.assertEqual(login, True)


class SwaggerTestCase(BaseTestCase):

    api_data = [
        'models',
        'basePath',
        'apis'
    ]

    def test_get_base(self):
        """Return a 403 response error with detail message."""
        resp = self.api_client.get('/api/docs/')
        self.assertEqual(resp.status_code, 200)
        resp_xml = self.api_client.get('/api/docs/api-docs/')
        self.assertEqual(resp_xml.status_code, 200)

    def test_get_metadata(self):
        resp = self.api_client.get('/api/docs/api-docs/api/metadata')
        data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(set(self.api_data) <= set(data))
        for collection in enumerate(data):
            self.assertIsNotNone(collection)

    def test_get_players(self):
        resp = self.api_client.get('/api/docs/api-docs/api/players')
        data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(set(self.api_data) <= set(data))
        for collection in enumerate(data):
            self.assertIsNotNone(collection)

    def test_get_playlists(self):
        resp = self.api_client.get('/api/docs/api-docs/api/playlists')
        data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(set(self.api_data) <= set(data))
        for collection in enumerate(data):
            self.assertIsNotNone(collection)

    def test_get_queues(self):
        resp = self.api_client.get('/api/docs/api-docs/api/queues')
        data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(set(self.api_data) <= set(data))
        for collection in enumerate(data):
            self.assertIsNotNone(collection)

    def test_get_users(self):
        resp = self.api_client.get('/api/docs/api-docs/api/users')
        data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(set(self.api_data) <= set(data))
        for collection in enumerate(data):
            self.assertIsNotNone(collection)
