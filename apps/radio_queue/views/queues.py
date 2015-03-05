# -*- coding: utf-8 -*-
"""Queue related views
"""
# third-party imports
from django.core.cache import cache
from rest_framework import permissions, viewsets
from rest_framework.response import Response

# local imports
from ..models import Queue
from ..serializers import QueueSerializer
from ..serializers import PaginatedQueueSerializer
from radio.exceptions import RecordDeleteFailed
from radio.exceptions import RecordNotFound
from radio.permissions import IsStaffOrOwnerToDelete
from radio.utils.cache import build_key
from radio.utils.pagination import paginate_queryset


class QueueViewSet(viewsets.ModelViewSet):
    """CRUD API endpoints that allow managing queue."""
    cache_key = build_key('queue-queryset')
    permission_classes = (IsStaffOrOwnerToDelete, permissions.IsAuthenticated)
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer

    def list(self, request):
        """Return a paginated list of queue json objects."""
        page = int(request.QUERY_PARAMS.get('page', 1))

        queryset = cache.get(self.cache_key)
        if queryset is None:
            queryset = Queue.objects.select_related('owner').all()
            cache.set(self.cache_key, queryset, 86400)

        response = paginate_queryset(
            PaginatedQueueSerializer, request, queryset, page)

        return Response(response)

    def destroy(self, request, *args, **kwargs):
        """Removes queue and its associated queue tracks from database.
        Returns a detail reponse.
        """
        try:
            queue = Queue.objects.get(id=kwargs['pk'])
        except:
            raise RecordNotFound

        try:
            cache.delete(self.cache_key)
            queue.delete()
        except:
            raise RecordDeleteFailed

        return Response({'detail': 'Queue successfully removed.'})

    def pre_save(self, obj):
        """Set the record owner as the current logged in user,
        when creating/updating a record.

        Remove the cached track list after a database record is updated.
        """
        obj.owner = self.request.user
        cache.delete(self.cache_key)
