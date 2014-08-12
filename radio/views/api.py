# -*- coding: utf-8 -*-
"""
Core radio API views.

The views in this module exist primarily to tie together the browsable APIs of
our seperate apps, there probably shouldn't be any substantial logic in here.
"""
# stdlib imports
import collections

# third-party imports
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer


class APIRootView(APIView):
    """
    The rehabradio API allows full control of all functionality. All clients,
    including the web frontends rely on this API for control of the system.

    Clients should use the metadata API to retrieve data about available songs.
    The metadata API coerces data from the available backends into a unified
    format that allows for easy interoperability and addition of new backends
    in future.

    Clients should use the playlist API to manage playlists.
    Owners of playlists can set various permissions,
    allowing certain users to perform certain actions on a playlist
    such as adding or removing tracks.
    """

    def get(self, request, format=None):
        response = collections.OrderedDict([
            ('endpoints', collections.OrderedDict([
                ('metadata', reverse('radio-data-api-root', request=request)),
                (
                    'playlists',
                    reverse('radio-playlists-list', request=request)
                ),
                ('queue', reverse('radio-queue-list', request=request)),
                ('users', reverse('radio-users-api-list', request=request)),
            ])),
        ])
        return Response(response)


class SwaggerView(APIView):
    """
    Swagger config
    """
    renderer_classes = (JSONRenderer,)

    def get(self, request, format=None):
        settings = {
            'basePath': 'http://localhost:8000/api/docs/api-docs',
            'swaggerVersion': '1.2',
            'apiVersion': '0.1',
            'apis': [
                {
                    'path': '/api/metadata',
                    'description': 'Search and store track data from \
                                        a list of sources'
                },
                {
                    'path': '/api/playlists',
                    'description': 'Manage playlists'
                },
                {
                    'path': '/api/queues',
                    'description': 'Manage queues'
                }
            ],
            'info': {
                'title': 'rehabradio API',
                'description': '<hr> \
                    The rehabradio API allows full control of all \
                    functionality. All clients, including the web \
                    frontends rely on this API for control of the \
                    system. Clients should use the metadata API to \
                    retrieve data about available songs. The \
                    metadata API coerces data from the available \
                    backends into a unified format that allows for \
                    easy interoperability and addition of new backends \
                    in future.<br /><br />\
                    Clients should use the playlist API to manage playlists. \
                    Owners of playlists can set various permissions, \
                    allowing certain users to perform certain actions on \
                    a playlist such as adding or removing tracks.\
                    <hr>',
                'termsOfServiceUrl': '',
                'contact': '',
                'license': '',
                'licenseUrl': ''
            }
        }
        return Response(settings)
