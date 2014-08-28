# stdlib imports
import json
import os
# third-party imports
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
# local imports
from .models import Player


class BaseTestCase(TestCase):
    """Load in default data for tests, and login user."""
    fixtures = ['radio/fixtures/testdata.json']
    factory = APIRequestFactory()
    api_client = APIClient()
    paginated_attrs = ('count', 'next', 'previous', 'results')
    player_attrs = (
        'id',
        'name',
        'location',
        'queue',
        'active',
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


class PlayerViewSetTestCase(BaseTestCase):
    """CRUD commands for the player database table"""
    def test_list_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get('/api/players/')
        self.assertEqual(resp.status_code, 403)

    def test_detail_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get('/api/players/3/')
        self.assertEqual(resp.status_code, 403)

    def test_list(self):
        """Return a paginated set of player json objects."""
        resp = self.api_client.get('/api/players/')
        data = json.loads(resp.content)
        players = data['results'][0]
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.paginated_attrs) <= set(data))
        self.assertTrue(set(self.player_attrs) <= set(players))

    def test_create(self):
        """Add a player to the database.
        Returns a player json object of the newly created record.
        """
        pass

    def test_create_with_empty_values(self):
        """Try to create a track, with a empty post data.
        Returns a 404 response with detail message.
        """
        pass

    def test_retrieve(self):
        """Return a player json object of a given record."""
        resp = self.api_client.get('/api/players/3/')
        data = json.loads(resp.content)

        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.player_attrs) <= set(data))

    def test_retrieve_with_bad_id(self):
        """Returns a 404 response with detail message."""
        resp = self.api_client.get('/api/players/100000/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 404)
        # Ensure the returned json keys match the expected
        self.assertEqual(data['detail'], u'The record could not be found.')

    def test_update(self):
        """Update a player from the database.
        Returns a player json object of the updated record.
        """
        pass

    def test_partial_update(self):
        """Update a single piece of player information from the database.
        Returns a player json object of the updated record.
        """
        pass

    def test_destroy(self):
        """Recursively remove a player and its associated player
        tracks from the database

        Returns a successful response, with a detail message.
        """
        pass

    def test_delete_with_bad_id(self):
        """Returns a 404 response with detail message."""
        pass
