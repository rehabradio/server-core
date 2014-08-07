# third-party imports
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

# local imports
from .views import (
    PlaylistViewSet,
    PlaylistTrackViewSet,
)


urlpatterns = patterns(
    '',
    url(
        r'^$', PlaylistViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }), name='radio-playlists-list'
    ),
    url(
        r'^(?P<pk>[0-9]+)/$',
        PlaylistViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='radio-playlists-detail'
    ),
    url(
        r'^(?P<playlist_id>[0-9]+)/tracks/$',
        PlaylistTrackViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        name='radio-playlists-tracks-list'
    ),
    url(
        r'^(?P<playlist_id>[0-9]+)/tracks/(?P<pk>[^/]+)$',
        PlaylistTrackViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name='radio-playlists-tracks-detail'
    ),
)

urlpatterns = format_suffix_patterns(urlpatterns)
