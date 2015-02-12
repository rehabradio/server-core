# third-party imports
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
# local imports
from .views.head import QueueHeadViewSet
from .views.history import QueueTrackHistoryViewSet
from .views.queues import QueueViewSet
from .views.tracks import QueueTrackViewSet


urlpatterns = patterns(
    '',
    url(
        r'^$',
        QueueViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }), name='radio-queue-list'
    ),
    url(
        r'^(?P<pk>[0-9]+)/$',
        QueueViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='radio-queue-detail'
    ),

    url(
        r'^(?P<queue_id>[0-9]+)/tracks/$',
        QueueTrackViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }), name='radio-queue-track-list'
    ),
    url(
        r'^(?P<queue_id>[0-9]+)/tracks/(?P<pk>[0-9]+)/$',
        QueueTrackViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='radio-queue-track-detail'
    ),

    url(
        r'^(?P<queue_id>[0-9]+)/head/$',
        QueueHeadViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='radio-queue-track-head'
    ),

    url(
        r'^(?P<queue_id>[0-9]+)/history/$',
        QueueTrackHistoryViewSet.as_view({'get': 'list'}),
        name='radio-queue-history-list'
    ),
    url(
        r'^(?P<queue_id>[0-9]+)/history/(?P<pk>[0-9]+)/$',
        QueueTrackHistoryViewSet.as_view({'get': 'retrieve'}),
        name='radio-queue-history-detail'
    ),
)

urlpatterns = format_suffix_patterns(urlpatterns)
