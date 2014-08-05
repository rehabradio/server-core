# third-party imports
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

# local imports
from .views import (
    QueueList,
    QueueAddTrack,
    QueueNextTrack,
    QueueTrackVote,
)


urlpatterns = patterns(
    '',
    url(
        r'^$',
        QueueList.as_view(),
        name='radio-queue-api'
    ),
    url(
        r'^active/$',
        QueueNextTrack.as_view(),
        name='radio-queue-api-active'
    ),
    url(
        r'^add/(?P<track_id>[^/]+)$',
        QueueAddTrack.as_view(),
        name='radio-queue-api-add'
    ),
    url(
        r'^vote/(?P<track_id>[0-9]+)/(?P<vote>[\-1]+)$',
        QueueTrackVote.as_view(),
        name='radio-data-tracks-vote'
    ),
)

urlpatterns = format_suffix_patterns(urlpatterns)
