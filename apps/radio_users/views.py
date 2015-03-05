# -*- coding: utf-8 -*-
"""User related views
"""
# Third party imports
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import viewsets

# Local imports
from .serializers import UserSerializer, PaginatedUserSerializer
from radio.utils.cache import build_key
from radio.utils.pagination import paginate_queryset


class UserViewSet(viewsets.ModelViewSet):
    """CRUD API endpoints that allow managing playlists.
    User must be signed in as admin.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        """Return a paginated list of queue json objects."""
        page = int(request.QUERY_PARAMS.get('page', 1))

        cache_key = build_key('users-queryset')
        response = cache.get(cache_key)
        if response:
            return Response(response)

        queryset = User.objects.exclude(profile__isnull=True)
        response = paginate_queryset(
            PaginatedUserSerializer, request, queryset, page)

        cache.set(cache_key, response, 86400)
        return Response(response)
