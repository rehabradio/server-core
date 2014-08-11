# third-party imports
from django.conf import settings
from django.conf.urls import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# local imports
from .views.api import APIRootView

# autodiscover all admin urls
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^api/docs/', include('rest_framework_swagger.urls')),
    # Django admin URLs
    url(r'^admin/', include(admin.site.urls)),
    # monitoring/admin URL for Django-RQ
    url(r'^django-rq/', include('django_rq.urls')),

    # API urls (browsable)
    url(r'^api/$', APIRootView.as_view(), name='radio-api-root'),
    url(r'^api/_auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/metadata/', include('radio_metadata.urls')),
    url(r'^api/playlists/', include('radio_playlists.urls')),
    url(r'^api/queues/', include('radio_queue.urls')),
    url(r'^api/users/', include('radio_users.urls')),
)

urlpatterns += staticfiles_urlpatterns()

# add some routes that are only active when DEBUG is turned on
if settings.DEBUG:

    # enable django-debug-toolbar only when we're running in debug mode
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
