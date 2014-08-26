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
        }), name='radio-players-list'
    ),
    url(
        r'^(?P<pk>[\w\-_]+)/$',
        PlayerViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='radio-players-detail'
    ),
    url(
        r'^(?P<pk>[\w\-_]+)/event/',
        PlayerViewSet.as_view({
            'post': 'mopidy_event',
        }), name='radio-players-mopidy-event'
    ),
    url(
        r'^(?P<pk>[\w\-_]+)/status/',
        PlayerViewSet.as_view({
            'post': 'mopidy_status',
        }), name='radio-players-mopidy-status'
    ),
)

urlpatterns = format_suffix_patterns(urlpatterns)
