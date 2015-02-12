# stdlib imports
import json

# local imports
from .test_base import BaseTestCase
from ..models import QueueTrack


class QueueHeadViewSetTestCase(BaseTestCase):
    def test_get(self):
        """Returns the queue track in position 1, in a given queue."""
        resp = self.api_client.get('/api/queues/1/head/')
        data = json.loads(resp.content)
        track = data['track']
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.queue_track_attrs) <= set(data))
        self.assertTrue(set(self.track_attrs) <= set(track))

    def test_radio(self):
        """Returns the queue track in position 1, in a given queue."""
        previous_track = None
        for i in range(10):
            get_resp = self.api_client.get('/api/queues/1/head/')
            data = json.loads(get_resp.content)
            # Ensure request was successful
            self.assertEqual(get_resp.status_code, 200)
            # Ensure the returned json keys match the expected
            self.assertTrue(set(self.queue_track_attrs) <= set(data))
            self.assertTrue(set(self.track_attrs) <= set(data['track']))
            self.assertNotEqual(previous_track, data['track'])
            previous_track = data['track']
            delete_resp = self.api_client.delete('/api/queues/1/head/')
            self.assertEqual(delete_resp.status_code, 200)

    def test_get_with_empty_queue(self):
        """Adds a random track to the queue, if queue is empty."""
        records_count = QueueTrack.objects.filter(queue=2).count()
        self.assertEqual(records_count, 0)

        resp = self.api_client.get('/api/queues/2/head/')
        data = json.loads(resp.content)

        # Ensure request was successful
        self.assertEqual(resp.status_code, 400)
        # Ensure the returned json keys match the expected
        self.assertEqual(data['detail'], u'This queue has no tracks.')

    def test_patch(self):
        """Update a the head track of a given queue.
        """
        # Count the number of records before the save
        existing_records_count = QueueTrack.objects.filter(
            queue=1).count()
        post_data = {
            'state': 'playing',
            'time_position': 12345
        }
        json_data = json.dumps(post_data, indent=2)

        resp = self.api_client.patch(
            '/api/queues/1/head/',
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

    def test_delete(self):
        """Remove a queue track from the database
        Returns a successful response, with a detail message.
        """
        # Count the number of records before the save
        existing_records_count = QueueTrack.objects.filter(
            queue=1
        ).count()

        resp = self.api_client.delete('/api/queues/1/head/')
        data = json.loads(resp.content)
        new_records_count = QueueTrack.objects.filter(queue=1).count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the record was removed from the database
        self.assertEqual(existing_records_count-1, new_records_count)
        # Ensure "detail" message is set, and the message matches expected
        self.assertEqual(
            data['detail'], u'Track successfully removed from queue.')

    def test_delete_with_empty_queue(self):
        """Returns a 404 response with detail message."""
        resp = self.api_client.delete('/api/queues/2/head/')
        data = json.loads(resp.content)
        # Ensure request was successful
        self.assertEqual(resp.status_code, 404)
        # Ensure the returned json keys match the expected
        self.assertEqual(data['detail'], u'The record could not be found.')
