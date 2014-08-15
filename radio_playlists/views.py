# third-party imports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import status, viewsets
from rest_framework.response import Response

# local imports
from .models import Playlist, PlaylistTrack
from .serializers import (
    PlaylistSerializer,
    PlaylistTrackSerializer,
    PaginatedPlaylistTrackSerializer
)
from radio.permissions import (
    IsOwnerOrReadOnly,
    IsOwnerOrPlaylistOwnerElseReadOnly
)
from radio_metadata.models import Track


def _reset_track_positions(playlist_id):
    """
    Once a record has been removed, reset the postions
    """
    records = PlaylistTrack.objects.filter(playlist_id=playlist_id)

    for (i, track) in enumerate(records):
        track.position = i+1
        track.save()


class PlaylistViewSet(viewsets.ModelViewSet):
    """
    CRUD API endpoints that allow managing playlists.
    For update and delete functions, user must be owner
    """
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Remove a playlist and its associated tracks from the database
        Returns a detail reponse
        """
        try:
            playlist = Playlist.objects.get(id=kwargs['pk'])
        except:
            response = {'detail': 'Playlist not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        try:
            playlist.delete()
        except:
            response = {
                'detail': 'Failed to remove playlist',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        return Response({'detail': 'playlist successfully removed'})

    def pre_save(self, obj):
        """
        Set user id, for each record saved/updated
        """
        obj.owner = self.request.user


class PlaylistTrackViewSet(viewsets.ModelViewSet):
    """
    CRUD API endpoints that allow managing playlist tracks.
    position -- Patch request param (int) - form
    """
    permission_classes = (IsOwnerOrPlaylistOwnerElseReadOnly,)
    queryset = PlaylistTrack.objects.all()
    serializer_class = PlaylistTrackSerializer

    def list(self, request, playlist_id=None):
        """
        Returns a paginated set of tracks in a given playlist
        """
        queryset = PlaylistTrack.objects.select_related().filter(playlist_id=playlist_id)
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
        serializer = PaginatedPlaylistTrackSerializer(
            users, context=serializer_context
        )
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Uses a track id to add a track to the playlist
        """
        track_id = request.POST['track']
        playlist_id = kwargs['playlist_id']
        total_playlist_records = PlaylistTrack.objects.filter(
            playlist=kwargs['playlist_id']
        ).count()

        try:
            playlist = PlaylistTrack.objects.create(
                track=Track.objects.get(id=track_id),
                playlist=Playlist.objects.get(id=playlist_id),
                position=total_playlist_records+1,
                owner=self.request.user
            )
        except:
            response = {'detail': 'Track could not be saved to playlist'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        new_playlist = PlaylistTrack.objects.filter(id=playlist.id).values()[0]
        return Response(new_playlist)

    def partial_update(self, request, *args, **kwargs):
        """
        Update a playlist track's position
        """
        try:
            playlist_track = PlaylistTrack.objects.get(id=kwargs['pk'])
            playlist_track.position = request.DATA['position']
            playlist_track.save()
        except:
            response = {'detail': 'Playlist track could not be updated'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        new_playlist = PlaylistTrack.objects.filter(
            id=playlist_track.id
        ).values()[0]

        return Response(new_playlist)

    def destroy(self, request, *args, **kwargs):
        """
        Removes playlist track from db and resets the remaining tracks position
        """
        try:
            playlist_track = PlaylistTrack.objects.get(id=kwargs['pk'])
            playlist_id = playlist_track.playlist.id
            playlist_track.delete()
            _reset_track_positions(playlist_id)
        except:
            response = {'detail': 'Playlist track not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        return Response({'detail': 'Track removed from playlist'})

    def pre_save(self, obj):
        """
        Set user id, for each record saved/updated
        """
        obj.owner = self.request.user
