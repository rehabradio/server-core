# local imports
from .test_base import BaseTestCase


class UserRootViewTestCase(BaseTestCase):

    def test_get(self):
        resp = self.api_client.get('/api/metadata/user/')
        self.assertEqual(resp.status_code, 200)


class UserAuthViewTestCase(BaseTestCase):
    """Ensure authentication requests are redirected to the respected third-party sites.
    """

    def test_get_spotify_redirect(self):
        resp = self.api_client.get('/api/metadata/user/authenticate/spotify/')
        self.assertEqual(resp.status_code, 302)

    def test_get_soundcloud_redirect(self):
        resp = self.api_client.get('/api/metadata/user/authenticate/soundcloud/')
        self.assertEqual(resp.status_code, 302)

    def test_get_youtube_redirect(self):
        resp = self.api_client.get('/api/metadata/user/authenticate/youtube/')
        self.assertEqual(resp.status_code, 302)

    def test_get_with_bad_backend(self):
        resp = self.api_client.get('/api/metadata/user/authenticate/test/')
        self.assertEqual(resp.status_code, 404)


class UserPlaylistViewSetTestCase(BaseTestCase):
    """Endpoints should return a list of playlists for a given third-party app.
    If user is not authenticated, then it will return a 403 response.
    """

    def test_list_soundcloud_with_no_oauth(self):
        resp = self.api_client.get('/api/metadata/user/playlists/soundcloud/')
        self.assertEqual(resp.status_code, 403)

    def test_list_spotify_with_no_oauth(self):
        resp = self.api_client.get('/api/metadata/user/playlists/spotify/')
        self.assertEqual(resp.status_code, 403)

    def test_list_youtube_with_no_oauth(self):
        resp = self.api_client.get('/api/metadata/user/playlists/youtube/')
        self.assertEqual(resp.status_code, 403)
