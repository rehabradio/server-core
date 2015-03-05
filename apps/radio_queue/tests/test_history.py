# stdlib imports
import json

# local imports
from .test_base import BaseTestCase


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
