from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.UserList.as_view(), name='radio-users-api-list'),
    url(r'^(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
)
