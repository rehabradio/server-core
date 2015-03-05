# stdlib imports
import json

# third-party imports
from django.db import transaction

# local imports
from .test_base import BaseTestCase
from ..models import Track


class TrackViewSetTestCase(BaseTestCase):
    """CRUD commands for the track database table.
    """

    def test_list_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get('/api/metadata/tracks/')
        self.assertEqual(resp.status_code, 403)

    def test_detail_auth(self):
        """Return a 403 response error with detail message."""
        self.api_client.logout()
        resp = self.api_client.get('/api/metadata/tracks/1/')
        self.assertEqual(resp.status_code, 403)

    def test_list(self):
        """Return a paginated set of track json objects."""
        track_attrs = self.track_attrs + ('id',)
        resp = self.api_client.get('/api/metadata/tracks/')
        data = json.loads(resp.content)
        tracks = data['results'][0]
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure the returned json keys match the expected
        self.assertTrue(set(self.paginated_attrs) <= set(data))
        self.assertTrue(set(track_attrs) <= set(tracks))

    def test_create_spotify(self):
        """Add a track to the database.
        Returns a track json object of the newly created record.
        """
        # Count the number of records before the save
        existing_records_count = Track.objects.all().count()
        post_data = {
            'source_type': 'spotify',
            'source_id': '7mitXLIMCflkhZiD34uEQI',
        }

        resp = self.api_client.post('/api/metadata/tracks/', data=post_data)
        new_records_count = Track.objects.all().count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure a new record was created in the database
        self.assertEqual(existing_records_count+1, new_records_count)

    def test_create_soundcloud(self):
        """Add a track to the database.
        Returns a track json object of the newly created record.
        """
        # Count the number of records before the save
        existing_records_count = Track.objects.all().count()
        post_data = {
            'source_type': 'soundcloud',
            'source_id': 153868082,
        }

        with transaction.atomic():
            resp = self.api_client.post('/api/metadata/tracks/', data=post_data)

        new_records_count = Track.objects.all().count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure a new record was created in the database
        self.assertEqual(existing_records_count+1, new_records_count)

    def test_create_youtube(self):
        """Add a track to the database.
        Returns a track json object of the newly created record.
        """
        # Count the number of records before the save
        existing_records_count = Track.objects.all().count()
        post_data = {
            'source_type': 'youtube',
            'source_id': 'StTqXEQ2l-Y',
        }

        with transaction.atomic():
            resp = self.api_client.post('/api/metadata/tracks/', data=post_data)

        new_records_count = Track.objects.all().count()
        # Ensure request was successful
        self.assertEqual(resp.status_code, 200)
        # Ensure a new record was created in the database
        self.assertEqual(existing_records_count+1, new_records_count)

    def test_create_with_bad_id(self):
        """Try to create a track, with a bad source_id.
        Returns a 404 response with detail message.
        """
        # Count the number of records before the save
        existing_records_count = Track.objects.all().count()
        post_data = {'source_type': 'spotify', 'source_id': 00}
        resp = self.api_client.post('/api/metadata/tracks/', data=post_data)
        data = json.loads(resp.content)
        new_records_count = Track.objects.all().count()

        # Ensure the request filed with a 404, and an error message is returned
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(existing_records_count, new_records_count)
        self.assertEqual(data['detail'], u'The record could not be found.')

    def test_create_with_bad_backend(self):
        """Returns a 404 response with detail message."""
        # Count the number of records before the save
        post_data = {
            'source_type': 'test',
            'source_id': '4bCOAuhvjsxbVBM5MM8oik',
        }
        resp = self.api_client.post('/api/metadata/tracks/', data=post_data)
        data = json.loads(resp.content)

        # Ensure the request filed with a 404, and an error message is returned
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['detail'], u'The record could not be found.')

    def test_retrieve(self):
        """Return a track json object of a given record."""
        track_attrs = self.track_attrs + ('id',)
        resp = self.api_client.get('/api/metadata/tracks/1/')
        data = json.loads(resp.content)

        # Ensure request was successful, and the correct data is returned.
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(set(track_attrs) <= set(data))

    def test_retrieve_with_bad_id(self):
        """Returns a 404 response with detail message."""
        resp = self.api_client.get('/api/metadata/tracks/100000/')
        data = json.loads(resp.content)

        # Ensure the request filed with a 404, and an error message is returned
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['detail'], u'Not found')

    def test_delete(self):
        """Remove a track from the database
        Returns a successful response, with a detail message.
        """
        # Count the number of records before the save
        existing_records_count = Track.objects.all().count()
        resp = self.api_client.delete('/api/metadata/tracks/2/')
        data = json.loads(resp.content)
        new_records_count = Track.objects.all().count()

        # Ensure request was successful, and the record is removed from the database.
        # Should return with a success message.
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(existing_records_count-1, new_records_count)
        self.assertEqual(data['detail'], 'Track successfully removed')

    def test_delete_with_bad_id(self):
        """Returns a 404 response with detail message."""
        resp = self.api_client.delete('/api/metadata/tracks/100000/')
        data = json.loads(resp.content)

        # Ensure the request filed with a 404, and an error message is returned
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['detail'], u'The record could not be found.')
