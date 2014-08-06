import json
from django.test import TestCase


class BaseTestCase(TestCase):
    fixtures = ['radio/fixtures/testdata.json']


class PlaylistViewSetTestCase(BaseTestCase):
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
