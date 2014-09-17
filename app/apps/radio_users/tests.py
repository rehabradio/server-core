# stdlib imports
import json
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
    user_attrs = (
        'id',
        'avatar',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_superuser',
        'is_staff',
        'last_login',
        'date_joined',
    )

    def setUp(self):
        """Ensure Auth is required and log in the test user."""
        username = os.environ.get('TEST_USERNAME', None)
        password = os.environ.get('TEST_PASSWORD', None)

        login = self.api_client.login(username=username, password=password)
        self.assertEqual(login, True)


class UserViewSetTestCase(BaseTestCase):
    """CRUD commands for the user database table"""
    def test_list_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get('/api/users/')
        self.assertEqual(resp.status_code, 403)

    def test_detail_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get('/api/users/1/')
        self.assertEqual(resp.status_code, 403)

    def test_list(self):
        """Return a paginated set of user json objects."""
        resp = self.api_client.get('/api/users/')
        data = json.loads(resp.content)
        users = data['results'][0]
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.paginated_attrs) <= set(data))
        self.assertTrue(set(self.user_attrs) <= set(users))

    def test_retrieve(self):
        """Return a user json object of a given record."""
        resp = self.api_client.get('/api/users/1/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.user_attrs) <= set(data))

    def test_retrieve_with_bad_id(self):
        """Returns a 404 response with detail message."""
        resp = self.api_client.get('/api/users/100000/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 404)
        # Ensure the returned json keys match the expected
        self.assertEqual(data['detail'], u'Not found')

    def test_create(self):
        """Add a player to the database.
        Returns a player json object of the newly created record.
        """
        post_data = {
            'username': 'tdduser',
            'password': 'test'
        }

        resp = self.api_client.post('/admin/auth/user/add/', data=post_data)
        # Ensure request was successful and user is redirected to player list
        self.assertEqual(resp.status_code, 200)

    def test_delete(self):
        """Returns a 200 response."""
        post_data = {'post': 'yes'}
        resp = self.api_client.post('/admin/auth/user/2/delete/', data=post_data)
        # Ensure request was successful
        self.assertRedirects(resp, '/admin/auth/user/')
