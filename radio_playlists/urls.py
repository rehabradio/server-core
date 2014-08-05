# third-party imports
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

# local imports
from .views import (
    PlaylistViewSet,
    PlaylistTrackViewSet,
    PlaylistTrackUpdateOrder,
)


urlpatterns = patterns(
    '',
    url(
        r'^$', PlaylistViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }), name='radio-playlists-api-list'
    ),
    url(
        r'^(?P<pk>[0-9]+)/$',
        PlaylistViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='radio-playlists-api-detail'
    ),
    url(
        r'^(?P<playlist>[0-9]+)/track/(?P<pk>[^/]+)$',
        PlaylistTrackViewSet.as_view({
            'get': 'retrieve',
            'delete': 'destroy',
        }),
        name='radio-playlists-api-track'
    ),
    url(
        r'^(?P<playlist>[0-9]+)/track/(?P<pk>[^/]+)/order/(?P<direction>[\-1]+)$',
        PlaylistTrackUpdateOrder.as_view(),
        name='radio-playlists-api-track-order'
    ),
)

urlpatterns = format_suffix_patterns(urlpatterns)
