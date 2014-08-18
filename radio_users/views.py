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
    """
    CRUD API endpoints that allow managing playlists.
    User must be staff to remove track from database
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    def list(self, request):
        """
        CRUD API endpoints that allow managing users.
        Admin permissions required
        """
        cache_key = u'userlist-{0}'.format(
            datetime.datetime.utcnow().strftime('%Y%m%d'),
        )
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

    def retrieve(self, request, pk=None):
        """
        CRUD API endpoints that allow managing users.
        Admin permissions required
        """
        cache_key = u'userdetail-{0}-{1}'.format(
            pk, datetime.datetime.utcnow().strftime('%Y%m%d'),
        )
        queryset = cache.get(cache_key)
        if queryset is None:
            users = User.objects.select_related('profile').get(id=pk)
            serializer = UserSerializer(users)
            queryset = serializer.data
            cache.set(cache_key, queryset, 86400)

        return Response(queryset)

    def post_save(self, user, created=False):
        """
        On creation, create a profile
        """
        if created:
            # Create an empty profile
            Profile.objects.create(user=user)
            # Update the cache
            cache_key = u'userlist-{0}'.format(
                datetime.datetime.utcnow().strftime('%Y%m%d'),
            )
            users = User.objects.select_related('profile').all()
            serializer = UserSerializer(users)
            queryset = serializer.data
            cache.set(cache_key, queryset, 86400)
