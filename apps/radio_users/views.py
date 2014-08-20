# -*- coding: utf-8 -*-
"""User related views
"""
# stdlib imports
import datetime
# Third party imports
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
# Local imports
from .models import Profile
from .serializers import UserSerializer, PaginatedUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """CRUD API endpoints that allow managing playlists.
    User must be signed in as admin.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    def _get_cache_key(self):
        """Build key used for caching the user list."""
        return 'userlist-{0}'.format(
            datetime.datetime.utcnow().strftime('%Y%m%d'),
        )

    def list(self, request):
        """Return a paginated list of queue json objects."""
        cache_key = self._get_cache_key()
        queryset = cache.get(cache_key)
        if queryset is None:
            users = User.objects.select_related('profile').all()
            serializer = UserSerializer(users)
            queryset = serializer.data
            cache.set(cache_key, queryset, 86400)

        paginator = Paginator(queryset, 20)

        page = request.QUERY_PARAMS.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            users = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            users = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        serializer = PaginatedUserSerializer(
            users, context=serializer_context
        )
        return Response(serializer.data)

    def post_save(self, user, created=False):
        """Remove the cached track list after a database record is updated.

        On creation, create a profile.
        """
        cache.delete(self._get_cache_key())
        if created:
            Profile.objects.create(user=user)

    def post_delete(self, user):
        """Remove the cached track list after a database record is removed."""
        cache.delete(self._get_cache_key())
