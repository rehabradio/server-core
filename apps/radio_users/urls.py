from django.conf.urls import patterns, url

from .views import UserViewSet

urlpatterns = patterns(
    '',
    url(
        r'^$',
        UserViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        name='radio-users-api-list'
    ),
    url(
        r'^(?P<pk>[^/]+)/$',
        UserViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name='radio-users-api-detail'
    ),
)
