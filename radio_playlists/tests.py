import json
from django.test import TestCase
from django.test.client import Client


class BaseTestCase(TestCase):
    fixtures = ['radio/fixtures/testdata.json']


class PlaylistViewSetTestCase(BaseTestCase):
    def setUp(self):
        self.client = Client()
        login = self.client.login(username='admin', password='redc@t9912')
        self.assertEqual(login, True)


    def test_list(self):
        result_attrs = (
            'count',
            'next',
            'previous',
            'results',
        )

        track_attrs = (
            'id',
            'name',
            'description',
        )

        resp = self.client.get('/api/playlists/')
        data = json.loads(resp.content)
        playlists = data['results'][0]

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(set(result_attrs) <= set(data))
        self.assertTrue(set(track_attrs) <= set(playlists))

    def test_create(self):
        post_data = {
            'name': 'test playlist',
            'description': 'a playlist for tdd',
        }

        resp = self.client.post('/api/playlists/', data=post_data)
        data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 201)
        self.assertRegexpMatches(str(data['id']), r'[0-9]+')
        self.assertEqual(data['name'], post_data['name'])
        self.assertEqual(data['description'], post_data['description'])


    def test_create_with_empty_values(self):
        post_data = {
            'name': '',
            'description': '',
        }

        resp = self.client.post('/api/playlists/', data=post_data)
        data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['name'], ['This field is required.'])
        self.assertEqual(data['description'], ['This field is required.'])

    def test_retrieve(self):
        pass

    def test_update(self):
        pass

    def test_partial_update(self):
        pass

    def test_destroy(self):
        pass


class PlaylistTrackViewSetTestCase(BaseTestCase):
    def test_list(self):
        pass

    def test_create(self):
        pass

    def test_retrieve(self):
        pass

    def test_update(self):
        pass

    def test_partial_update(self):
        pass

    def test_destroy(self):
        pass
