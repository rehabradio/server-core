from django.conf.urls import patterns, url

from .views import UserViewSet

urlpatterns = patterns(
    '',
    url(
        r'^$',
        UserViewSet.as_view({'get': 'list'}),
        name='radio-users-api-list'
    ),
    url(
        r'^(?P<pk>[^/]+)/$',
        UserViewSet.as_view({'get': 'retrieve'}),
        name='radio-users-api-detail'
    ),
)
