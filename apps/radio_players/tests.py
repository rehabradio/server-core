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
        # Count the number of records before the save
        existing_records_count = Player.objects.all().count()

        post_data = {
            'name': 'TDD player',
            'location': 'test env',
            'queue': 1,
        }

        resp = self.api_client.post(
            '/admin/radio_players/player/add/', data=post_data)
        new_records_count = Player.objects.all().count()

        # Ensure request was successful and user is redirected to player list
        self.assertRedirects(resp, '/admin/radio_players/player/')
        # Ensure a new record was created in the database
        self.assertEqual(existing_records_count+1, new_records_count)

    def test_create_with_active_not_unique(self):
        """Try to create a track, with a empty post data.
        Returns a 404 response with detail message.
        """
        # Count the number of records before the save
        existing_records_count = Player.objects.all().count()

        post_data = {
            'name': 'TDD player',
            'location': 'test env',
            'queue': 1,
            'active': True,
        }
        resp = self.api_client.post(
            '/admin/radio_players/player/add/',
            data=post_data
        )
        new_records_count = Player.objects.all().count()

        # Ensure error message was returned
        self.assertContains(
            resp, "A player is already active on the selected queue")
        # Ensure a new record was not created in the database
        self.assertEqual(existing_records_count, new_records_count)

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
