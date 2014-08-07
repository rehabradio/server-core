# stdlib imports
import collections

# third-party imports
from rest_framework import status, viewsets
from rest_framework.response import Response

# local imports
from .models import Playlist, PlaylistTrack
from .serializers import PlaylistSerializer, PlaylistTrackSerializer


def _reset_track_positions(playlist_id):
    """
    Once a record has been removed, reset the postions
    """
    records = PlaylistTrack.objects.filter(playlist_id=playlist_id)

    for (i, track) in enumerate(records):
        track.position = i+1
        track.save()


def _build_track(record):
    """
    Builds a ordered object to be returned to the client
    """
    # Fetch all track data
    track = record.track
    # Put all the track data into a nice singular dictionary
    track = collections.OrderedDict([
        ('id', record.id),
        ('track_id', track.id),
        ('source_id', track.source_id),
        ('source_type', track.source_type),
        ('name', track.name),
        ('artists', track.artists.all().values()),
        ('duration_ms', track.duration_ms),
        ('track_number', track.track_number),
        ('preview_url', track.preview_url),
        ('position', record.position),
        ('album', unicode(track.album)),
        ('image_small', track.image_small),
        ('image_medium', track.image_medium),
        ('image_large', track.image_large),
    ])
    return track


class PlaylistViewSet(viewsets.ModelViewSet):
    """
    CRUD API endpoints that allow managing playlists.
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    # Removes playlist from db (Cascading)
    def destroy(self, request, *args, **kwargs):
        """
        Removes playlist from database, and returns a detail reponse
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
    """
    queryset = PlaylistTrack.objects.all()
    serializer_class = PlaylistTrackSerializer

    def list(self, request, *args, **kwargs):
        """
        Returns a list of all the playlist tracks with track data
        """
        try:
            playlist = Playlist.objects.get(id=kwargs['playlist_id'])
        except:
            response = {
                'detail': 'Playlist not found',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        # Grab all the associated tracks
        db_tracks = PlaylistTrack.objects.filter(playlist_id=playlist)
        # Loop through each track, to restructure and populate associate data
        tracks = []
        for (counter, record) in enumerate(db_tracks):
            # Build out the track data
            trackData = _build_track(record)
            tracks.append(trackData)

        # Return data
        orderedPlaylist = collections.OrderedDict([
            ('count', len(tracks)),
            ('next', None),
            ('previous', None),
            ('results', tracks),
        ])

        return Response(orderedPlaylist)

    def create(self, request, *args, **kwargs):
        """
        Uses a track id to add a track to the playlist
        """
        post_data = {
            'track': request.POST['track'],
            'playlist': kwargs['playlist_id'],
            'position': int(self.queryset.count())+1
        }

        serializer = self.serializer_class(data=post_data)
        if serializer.is_valid():
            serializer.save()
        else:
            response = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return Response(post_data)

    def retrieve(self, request, *args, **kwargs):
        """
        Returns a playlist track with track data
        """
        try:
            playlist_track = PlaylistTrack.objects.get(id=kwargs['pk'])
            trackData = _build_track(playlist_track)
        except:
            response = {
                'detail': 'Playlist track not found',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        return Response(trackData)

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
            response = {
                'detail': 'Playlist track not found',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        return Response({'detail': 'Track removed from playlist'})

    def pre_save(self, obj):
        """
        Set user id, for each record saved/updated
        """
        obj.owner = self.request.user
