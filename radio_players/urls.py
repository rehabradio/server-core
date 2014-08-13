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
        r'^(?P<pk>[0-9]+)/$',
        PlayerViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='radio-players-detail'
    ),
)

urlpatterns = format_suffix_patterns(urlpatterns)
