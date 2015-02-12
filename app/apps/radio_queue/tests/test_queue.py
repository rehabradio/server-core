# stdlib imports
import json

# local imports
from .test_base import BaseTestCase
from ..models import Queue


class QueueViewSetTestCase(BaseTestCase):
    """CRUD commands for the queue database table"""
    def test_list_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get('/api/queues/')
        self.assertEqual(resp.status_code, 403)

    def test_detail_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get('/api/queues/1/')
        self.assertEqual(resp.status_code, 403)

    def test_list(self):
        """Return a paginated set of queue json objects."""
        resp = self.api_client.get('/api/queues/')
        data = json.loads(resp.content)
        queues = data['results'][0]
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.paginated_attrs) <= set(data))
        self.assertTrue(set(self.queue_attrs) <= set(queues))

    def test_create_with_track(self):
        """Add a queue track to the database.
        params - track

        Returns a queue track json object of the newly created record.
        """
        # Count the number of records before the save
        existing_records_count = Queue.objects.count()
        post_data = {
            'name': 'tmp queue',
            'description': 'test'
        }

        resp = self.api_client.post('/api/queues/', data=post_data)
        data = json.loads(resp.content)

        new_records_count = Queue.objects.count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 201)
        # Ensure a new record was created in the database
        self.assertEqual(existing_records_count+1, new_records_count)
        # Ensure the returned json keys match the expected
        self.assertRegexpMatches(str(data['id']), r'[0-9]+')
        self.assertEqual(data['name'], post_data['name'])
        self.assertEqual(data['description'], post_data['description'])

    def test_destroy(self):
        """Recursively remove a queue and its associated queue
        tracks from the database

        Returns a successful response, with a detail message.
        """
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
        self.assertEqual(data['detail'], u'Queue successfully removed.')

    def test_delete_with_bad_id(self):
        """Returns a 404 response with detail message."""
        resp = self.api_client.delete('/api/queues/100000/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 404)
        # Ensure the returned json keys match the expected
        self.assertEqual(data['detail'], u'The record could not be found.')
