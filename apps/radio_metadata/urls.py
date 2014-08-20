# third-party imports
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
# local imports
from .views import (
    LookupRootView,
    LookupView,
    MetadataAPIRootView,
    SearchRootView,
    SearchView,
    TrackViewSet,
)

urlpatterns = patterns(
    '',
    url(r'^$', MetadataAPIRootView.as_view(), name='radio-data-api-root'),
    url(r'^lookup/$', LookupRootView.as_view(), name='radio-data-lookup-root'),
    url(
        r'^lookup/(?P<source_type>[^/]+)/(?P<source_id>[^/]+)/$',
        LookupView.as_view(), name='radio-data-lookup'
    ),
    url(r'^search/$', SearchRootView.as_view(), name='radio-data-search-root'),
    url(
        r'^search/(?P<source_type>[^/]+)/$',
        SearchView.as_view(), name='radio-data-search'
    ),
    url(
        r'^tracks/$',
        TrackViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        name='radio-data-tracks-list'
    ),
    url(
        r'^tracks/(?P<pk>[^/]+)/$',
        TrackViewSet.as_view({
            'get': 'retrieve',
            'delete': 'destroy',
        }),
        name='radio-data-tracks-detail'
    ),
)

urlpatterns = format_suffix_patterns(urlpatterns)
