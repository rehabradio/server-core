# third-party imports
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

# local imports
from .views import PlayerViewSet


urlpatterns = patterns(
    '',
    url(
        r'^$',
        PlayerViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }), name='radio-player-list'
    ),
    url(
        r'^(?P<pk>[0-9]+)/$',
        PlayerViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='radio-player-detail'
    ),
    url(
        r'^(?P<pk>[0-9]+)/hook/(?P<queue_id>[0-9]+)$',
        PlayerViewSet.as_view(), name='radio-player-hook'
    ),
    url(
        r'^(?P<pk>[0-9]+)/listen/(?P<queue_id>[0-9]+)$',
        PlayerViewSet.as_view(), name='radio-player-listen'
    ),
)

urlpatterns = format_suffix_patterns(urlpatterns)
