# stdlib imports
import json
import os
# third-party imports
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
# local imports
from .models import User


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

    def test_create(self):
        """Add a user to the database.
        Returns a user json object of the newly created record.
        """
        # Count the number of records before the save
        existing_records_count = User.objects.all().count()
        post_data = {
            'username': 'testuser',
            'password': 'password',
        }

        resp = self.api_client.post('/api/users/', data=post_data)
        data = json.loads(resp.content)
        new_records_count = User.objects.all().count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 201)
        # Ensure a new record was created in the database
        self.assertEqual(existing_records_count+1, new_records_count)
        # Ensure the returned json keys match the expected
        self.assertRegexpMatches(str(data['id']), r'[0-9]+')
        self.assertEqual(data['username'], post_data['username'])
        self.assertTrue(set(self.user_attrs) <= set(data))

    def test_create_with_empty_values(self):
        """Try to create a track, with a empty post data.
        Returns a 404 response with detail message.
        """
        # Count the number of records before the save
        existing_records_count = User.objects.all().count()
        post_data = {
            'username': '',
            'password': '',
        }

        resp = self.api_client.post('/api/users/', data=post_data)
        data = json.loads(resp.content)
        new_records_count = User.objects.all().count()
        # Ensure request failed
        self.assertEqual(resp.status_code, 400)
        # Ensure a new record was not added to the database
        self.assertEqual(existing_records_count, new_records_count)
        # Ensure validation flags where raised for each field
        self.assertEqual(data['username'], ['This field is required.'])
        self.assertEqual(data['password'], ['This field is required.'])

    def test_retrieve(self):
        """Return a user json object of a given record."""
        resp = self.api_client.get('/api/users/12/')
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

    def test_partial_update(self):
        """Update a single piece of user information from the database.
        Returns a user json object of the updated record.
        """
        # Count the number of records before the save
        existing_records_count = User.objects.all().count()
        post_data = {'email': 'frank@test.com'}

        resp = self.api_client.patch('/api/users/12/', data=post_data)
        data = json.loads(resp.content)
        new_records_count = User.objects.all().count()

        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure a the record was updated
        # and a new records was not added to the database
        self.assertEqual(existing_records_count, new_records_count)
        self.assertEqual(data['email'], post_data['email'])

    def test_destroy(self):
        """Recursively remove a user and its associated user
        tracks from the database

        Returns a successful response, with a detail message.
        """
        # Count the number of records before the save
        existing_records_count = User.objects.all().count()

        resp = self.api_client.delete('/api/users/12/')
        new_records_count = User.objects.all().count()

        # Ensure request was successful
        self.assertEqual(resp.status_code, 204)
        # Ensure the record was removed from the database
        self.assertEqual(existing_records_count-1, new_records_count)

    def test_delete_with_bad_id(self):
        """Returns a 404 response with detail message."""
        resp = self.api_client.delete('/api/users/100000/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 404)
        # Ensure the returned json keys match the expected
        self.assertEqual(data['detail'], u'Not found')
