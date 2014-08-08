import json
import os

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient

from .models import Queue, QueueTrack, QueueTrackHistory
from radio_metadata.models import Track


class BaseTestCase(TestCase):
    """
    Load in default data for tests
    """
    fixtures = ['radio/fixtures/testdata.json']
    factory = APIRequestFactory()
    api_client = APIClient()

    """
    Log in a user
    """
    def setUp(self):
        username = os.environ.get('TEST_USERNAME', None)
        password = os.environ.get('TEST_PASSWORD', None)
        login = self.api_client.login(username=username, password=password)
        self.assertEqual(login, True)


class QueueViewSetTestCase(BaseTestCase):
    """
    Retrieve a list of all queues in database
    """
    def test_list(self):
        expected_attrs = (
            'count',
            'next',
            'previous',
            'results',
        )

        expected_results_attrs = (
            'id',
            'name',
            'description',
            'owner',
            'created',
            'updated',
        )

        resp = self.api_client.get('/api/queues/')
        data = json.loads(resp.content)
        queues = data['results'][0]

        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(expected_attrs) <= set(data))
        self.assertTrue(set(expected_results_attrs) <= set(queues))

    """
    Create a queue
    """
    def test_create(self):
        # Count the number of records before the save
        existing_records_count = Queue.objects.all().count()
        post_data = {
            'name': 'rehab',
            'description': 'test'
        }

        resp = self.api_client.post('/api/queues/', data=post_data)
        data = json.loads(resp.content)
        new_records_count = Queue.objects.all().count()

        # Ensure request was successful
        self.assertEqual(resp.status_code, 201)
        # Ensure a new record was created in the database
        self.assertEqual(existing_records_count+1, new_records_count)
        # Ensure the returned json keys match the expected
        self.assertRegexpMatches(str(data['id']), r'[0-9]+')
        self.assertEqual(data['name'], post_data['name'])
        self.assertEqual(data['description'], post_data['description'])

    """
    Create a queue with no data
    """
    def test_create_with_empty_values(self):
        # Count the number of records before the save
        existing_records_count = Queue.objects.all().count()

        resp = self.api_client.post('/api/queues/', data=[])
        data = json.loads(resp.content)
        new_records_count = Queue.objects.all().count()

        # Ensure request failed
        self.assertEqual(resp.status_code, 400)
        # Ensure a new record was not added to the database
        self.assertEqual(existing_records_count, new_records_count)
        # Ensure validation flags where raised for each field
        self.assertEqual(data['name'], ['This field is required.'])
        self.assertEqual(data['description'], ['This field is required.'])

    """
    Retrieve a playlist and its associated tracks
    """
    def test_retrieve(self):
        expected_attrs = (
            'id',
            'name',
            'description',
        )

        resp = self.api_client.get('/api/queues/1/')
        data = json.loads(resp.content)

        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(expected_attrs) <= set(data))

    """
    Update a playlist's data
    """
    def test_update(self):
        # Count the number of records before the save
        existing_records_count = Queue.objects.all().count()
        post_data = {
            'name': 'updated playlist',
            'description': 'playlist is now updated',
        }

        resp = self.api_client.put('/api/queues/1/', data=post_data)
        new_record = Queue.objects.filter(id=1).values()[0]
        new_records_count = Queue.objects.all().count()

        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure a the record was updated
        # and a new records was not added to the database
        self.assertEqual(existing_records_count, new_records_count)
        self.assertEqual(new_record['name'], post_data['name'])
        self.assertEqual(new_record['description'], post_data['description'])

    """
    Update a single piece of playlist's data
    """
    def test_partial_update(self):
        # Count the number of records before the save
        existing_records_count = Queue.objects.all().count()
        post_data = {
            'name': 'patched playlist',
        }

        resp = self.api_client.patch('/api/queues/1/', data=post_data)
        new_record = Queue.objects.filter(id=1).values()[0]
        new_records_count = Queue.objects.all().count()

        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure a the record was updated
        # and a new records was not added to the database
        self.assertEqual(existing_records_count, new_records_count)
        self.assertEqual(new_record['name'], post_data['name'])

    """
    Cascade remove a playlist from the database
    """
    def test_destroy(self):
        # Count the number of records before the save
        existing_records_count = Queue.objects.all().count()

        resp = self.api_client.delete('/api/queues/1/')
        data = json.loads(resp.content)
        new_records_count = Queue.objects.all().count()

        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the record was removed from the database
        self.assertEqual(existing_records_count-1, new_records_count)
        # Ensure "detail" message is set, and the message matches expected
        self.assertEqual(data['detail'], 'Queue successfully removed')
