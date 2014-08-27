# stdlib imports
import json
import os
# third-party imports
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
# local imports
from .models import Queue, QueueTrack


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return [obj.real, obj.imag]
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)



class BaseTestCase(TestCase):
    """Load in default data for tests, and login user."""
    fixtures = ['radio/fixtures/testdata.json']
    factory = APIRequestFactory()
    api_client = APIClient()
    paginated_attrs = ('count', 'next', 'previous', 'results')
    queue_attrs = ('id', 'name', 'description', 'created', 'updated')
    queue_track_attrs = ('id', 'track', 'position', 'owner')
    track_attrs = (
        'id',
        'source_type',
        'source_id',
        'name',
        'artists',
        'album',
        'duration_ms',
        'preview_url',
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

    def test_create(self):
        """Add a queue to the database.
        Returns a queue json object of the newly created record.
        """
        # Count the number of records before the save
        existing_records_count = Queue.objects.all().count()
        post_data = {
            'name': 'test queue',
            'description': 'a queue for tdd',
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
        self.assertTrue(set(self.queue_attrs) <= set(data))

    def test_create_with_empty_values(self):
        """Try to create a track, with a empty post data.
        Returns a 404 response with detail message.
        """
        # Count the number of records before the save
        existing_records_count = Queue.objects.all().count()
        post_data = {
            'name': '',
            'description': '',
        }

        resp = self.api_client.post('/api/queues/', data=post_data)
        data = json.loads(resp.content)
        new_records_count = Queue.objects.all().count()
        # Ensure request failed
        self.assertEqual(resp.status_code, 400)
        # Ensure a new record was not added to the database
        self.assertEqual(existing_records_count, new_records_count)
        # Ensure validation flags where raised for each field
        self.assertEqual(data['name'], ['This field is required.'])
        self.assertEqual(data['description'], ['This field is required.'])

    def test_retrieve(self):
        """Return a queue json object of a given record."""
        resp = self.api_client.get('/api/queues/1/')
        data = json.loads(resp.content)

        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.queue_attrs) <= set(data))

    def test_retrieve_with_bad_id(self):
        """Returns a 404 response with detail message."""
        resp = self.api_client.get('/api/queues/100000/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 404)
        # Ensure the returned json keys match the expected
        self.assertEqual(data['detail'], u'Not found')

    def test_update(self):
        """Update a queue from the database.
        Returns a queue json object of the updated record.
        """
        # Count the number of records before the save
        existing_records_count = Queue.objects.all().count()
        post_data = {
            'name': 'Updated queue',
            'description': 'Queue is now updated',
        }

        resp = self.api_client.put('/api/queues/1/', data=post_data)
        data = json.loads(resp.content)
        new_records_count = Queue.objects.all().count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure a the record was updated
        # and a new records was not added to the database
        self.assertEqual(existing_records_count, new_records_count)
        self.assertEqual(data['name'], post_data['name'])
        self.assertEqual(data['description'], post_data['description'])

    def test_partial_update(self):
        """Update a single piece of queue information from the database.
        Returns a queue json object of the updated record.
        """
        # Count the number of records before the save
        existing_records_count = Queue.objects.all().count()
        post_data = {'name': 'patched queue'}

        resp = self.api_client.patch('/api/queues/1/', data=post_data)
        data = json.loads(resp.content)
        new_records_count = Queue.objects.all().count()

        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure a the record was updated
        # and a new records was not added to the database
        self.assertEqual(existing_records_count, new_records_count)
        self.assertEqual(data['name'], post_data['name'])

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


class QueueTrackViewSetTestCase(BaseTestCase):
    """CRUD commands for the queue_track database table."""
    def test_list_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get('/api/queues/1/tracks/')
        self.assertEqual(resp.status_code, 403)

    def test_detail_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get('/api/queues/1/tracks/1/')
        self.assertEqual(resp.status_code, 403)

    def test_list(self):
        """Return a paginated set of queue track json objects."""
        resp = self.api_client.get('/api/queues/1/tracks/')
        data = json.loads(resp.content)
        queue_tracks = data['results'][0]
        track = queue_tracks['track']
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.paginated_attrs) <= set(data))
        self.assertTrue(set(self.queue_track_attrs) <= set(queue_tracks))
        self.assertTrue(set(self.track_attrs) <= set(track))

    def test_create(self):
        """Add a queue track to the database.
        params - track

        Returns a queue track json object of the newly created record.
        """
        # Count the number of records before the save
        existing_records_count = QueueTrack.objects.filter(
            queue=1
        ).count()
        post_data = {
            'track': 3,
        }

        resp = self.api_client.post('/api/queues/1/tracks/', data=post_data)
        data = json.loads(resp.content)
        new_records_count = QueueTrack.objects.filter(queue=1).count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure a new record was created in the database
        self.assertEqual(existing_records_count+1, new_records_count)
        # Ensure the returned json keys match the expected
        self.assertRegexpMatches(str(data['id']), r'[0-9]+')
        self.assertEqual(data['track']['id'], post_data['track'])
        self.assertEqual(data['position'], int(new_records_count))

    def test_create_with_empty_values(self):
        """Try to create a track, empty post variables.
        Returns a 404 response with detail message.
        """
        # Count the number of records before the save
        existing_records_count = QueueTrack.objects.filter(
            queue=1
        ).count()
        post_data = {
            'track': None,
        }

        resp = self.api_client.post('/api/queues/1/tracks/', data=post_data)
        data = json.loads(resp.content)
        new_records_count = QueueTrack.objects.filter(queue=1).count()

        # Ensure request failed
        self.assertEqual(resp.status_code, 400)
        # Ensure a new record was not added to the database
        self.assertEqual(existing_records_count, new_records_count)
        # Ensure validation flags where raised for each field
        self.assertEqual(data['detail'], u'The record could not be saved.')

    def test_retrieve(self):
        """Return a track json object of a given record."""
        resp = self.api_client.get('/api/queues/1/tracks/3/')
        data = json.loads(resp.content)
        track = data['track']
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.queue_track_attrs) <= set(data))
        self.assertTrue(set(self.track_attrs) <= set(track))

    def test_retrieve_with_bad_id(self):
        """Returns a 404 response with detail message."""
        resp = self.api_client.get('/api/queues/1/tracks/100000/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 404)
        # Ensure the returned json keys match the expected
        self.assertEqual(data['detail'], u'Not found')

    def test_partial_update(self):
        """Update a queue track's position.
        Returns a queue track json object of the updated record.
        """
        # Count the number of records before the save
        existing_records_count = QueueTrack.objects.filter(
            queue=1
        ).count()
        post_data = {'position': 33}

        resp = self.api_client.patch(
            '/api/queues/1/tracks/3/',
            data=post_data
        )
        data = json.loads(resp.content)
        new_records_count = QueueTrack.objects.filter(queue=1).count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure a new record was created in the database
        self.assertEqual(existing_records_count, new_records_count)
        # Ensure the returned json keys match the expected
        self.assertEqual(int(data['position']), post_data['position'])

    def test_delete(self):
        """Remove a queue track from the database
        Returns a successful response, with a detail message.
        """
        # Count the number of records before the save
        existing_records_count = QueueTrack.objects.filter(
            queue=1
        ).count()

        resp = self.api_client.delete('/api/queues/1/tracks/3/')
        data = json.loads(resp.content)
        new_records_count = QueueTrack.objects.filter(queue=1).count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the record was removed from the database
        self.assertEqual(existing_records_count-1, new_records_count)
        # Ensure "detail" message is set, and the message matches expected
        self.assertEqual(
            data['detail'],
            u'Track successfully removed from queue.'
        )

    def test_delete_with_bad_id(self):
        """Returns a 404 response with detail message."""
        resp = self.api_client.delete('/api/queues/1/tracks/100000/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 404)
        # Ensure the returned json keys match the expected
        self.assertEqual(data['detail'], u'The record could not be found.')

    def test_head(self):
        """Returns the queue track in position 1, in a given queue."""
        resp = self.api_client.get('/api/queues/1/head/')
        data = json.loads(resp.content)
        track = data['track']
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.queue_track_attrs) <= set(data))
        self.assertTrue(set(self.track_attrs) <= set(track))

    def test_head_with_empty_queue(self):
        """Return the queue track in position 1, in a given queue."""
        resp = self.api_client.get('/api/queues/2/head/')
        data = json.loads(resp.content)
        track = data['track']
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.queue_track_attrs) <= set(data))
        self.assertTrue(set(self.track_attrs) <= set(track))

    def test_head_status(self):
        """Update a the head track of a given queue.
        """
        # Count the number of records before the save
        existing_records_count = QueueTrack.objects.filter(
            queue=1
        ).count()
        post_data = {
            'state': 'playing',
            'time_position': 12345
        }
        json_data = json.dumps(post_data, cls=ComplexEncoder, indent=2)

        resp = self.api_client.patch(
            '/api/queues/1/head/status/',
            data=json_data,
            format='json'
        )

        data = json.loads(resp.content)
        new_records_count = QueueTrack.objects.filter(queue=1).count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure a new record was created in the database
        self.assertEqual(existing_records_count, new_records_count)
        # Ensure the returned json keys match the expected
        self.assertEqual(data['state'], post_data['state'])
        self.assertEqual(
            int(data['time_position']), post_data['time_position'])

    def test_head_events(self):
        """Update time position value of the head track in a given queue.
        """
        # Count the number of records before the save
        existing_records_count = QueueTrack.objects.filter(
            queue=1
        ).count()
        post_data = {'time_position': 12345}
        json_data = json.dumps(post_data, cls=ComplexEncoder, indent=2)

        resp = self.api_client.patch(
            '/api/queues/1/head/events/seeked/',
            data=json_data,
            format='json'
        )
        data = json.loads(resp.content)
        new_records_count = QueueTrack.objects.filter(queue=1).count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure a new record was created in the database
        self.assertEqual(existing_records_count, new_records_count)
        # Ensure the returned json keys match the expected
        self.assertEqual(
            int(data['time_position']), post_data['time_position'])

    def test_head_pop(self):
        """Remove a queue track from the database
        Returns a successful response, with a detail message.
        """
        # Count the number of records before the save
        existing_records_count = QueueTrack.objects.filter(
            queue=1
        ).count()

        resp = self.api_client.delete('/api/queues/1/head/pop/')
        data = json.loads(resp.content)
        new_records_count = QueueTrack.objects.filter(queue=1).count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the record was removed from the database
        self.assertEqual(existing_records_count-1, new_records_count)
        # Ensure "detail" message is set, and the message matches expected
        self.assertEqual(
            data['detail'], u'Track successfully removed from queue.')

    def test_head_pop_with_empty_queue(self):
        """Returns a 404 response with detail message."""
        resp = self.api_client.delete('/api/queues/2/head/pop/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 404)
        # Ensure the returned json keys match the expected
        self.assertEqual(data['detail'], u'The record could not be found.')


class QueueTrackHistoryViewSetTestCase(BaseTestCase):
    """CRUD commands for the queue_history database table."""
    def test_list_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get('/api/queues/1/history/')
        self.assertEqual(resp.status_code, 403)

    def test_detail_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get('/api/queues/1/history/1/')
        self.assertEqual(resp.status_code, 403)

    def test_list(self):
        """Return a paginated set of queue track history json objects."""
        history_attrs = (
            'id',
            'track',
            'queue',
            'owner',
            'created',
        )

        resp = self.api_client.get('/api/queues/1/history/')
        data = json.loads(resp.content)
        queues = data['results'][0]
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.paginated_attrs) <= set(data))
        self.assertTrue(set(history_attrs) <= set(queues))

    def test_retrieve(self):
        """Return a queue track history json object."""
        history_attrs = (
            'id',
            'track',
            'queue',
            'owner',
            'created',
        )

        resp = self.api_client.get('/api/queues/1/history/1/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(history_attrs) <= set(data))
