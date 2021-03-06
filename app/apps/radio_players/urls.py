# third-party imports
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

# local imports
from .views import PlayerViewSet


urlpatterns = patterns(
    '',
    url(
        r'^$',
        PlayerViewSet.as_view({'get': 'list'}),
        name='radio-players-list'
    ),
    url(
        r'^(?P<pk>[0-9]+)/$',
        PlayerViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
        }),
        name='radio-players-detail'
    ),
    url(
        r'^(?P<token>[\w\-_]+)/$',
        PlayerViewSet.as_view({
            'get': 'retrieve'
        }),
        name='radio-players-detail'
    ),
)

urlpatterns = format_suffix_patterns(urlpatterns)
