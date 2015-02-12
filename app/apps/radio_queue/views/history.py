# -*- coding: utf-8 -*-
"""Queue history related views
"""
# third-party imports
from rest_framework import viewsets
from rest_framework.response import Response

# local imports
from ..models import QueueTrackHistory
from ..serializers import QueueTrackHistorySerializer
from ..serializers import PaginatedQueueTrackHistorySerializer
from radio.utils.pagination import paginate_queryset


class QueueTrackHistoryViewSet(viewsets.ModelViewSet):
    """CRUD API endpoints that allow managing queue history tracks."""
    queryset = QueueTrackHistory.objects.all()
    serializer_class = QueueTrackHistorySerializer

    def list(self, request, queue_id=None):
        """Return a paginated list of historic queue track json objects."""
        page = int(request.QUERY_PARAMS.get('page', 1))

        queryset = QueueTrackHistory.objects.prefetch_related(
            'track', 'track__artists', 'track__album',
            'track__owner', 'owner'
        ).filter(queue_id=queue_id)

        response = paginate_queryset(
            PaginatedQueueTrackHistorySerializer, request, queryset, page)

        return Response(response)
