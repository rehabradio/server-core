# stdlib imports
import collections

# third-party imports
from rest_framework import generics, status, viewsets
from rest_framework.reverse import reverse
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
        # Artists is a list of the artist names
        ('artists', [{'name': artist.name} for artist in track.artists.all()]),
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

    # Set user id, for each record saved
    def pre_save(self, obj):
        obj.owner = self.request.user


class PlaylistTrackViewSet(viewsets.ModelViewSet):
    """
    CRUD API endpoints that allow managing playlist tracks.
    """
    queryset = PlaylistTrack.objects.all()
    serializer_class = PlaylistTrackSerializer

    def list(self, request, *args, **kwargs):
        try:
            playlist = Playlist.objects.get(id=kwargs['playlist_id'])
        except:
            response = {
                'message': 'Playlist not found',
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

    def retrieve(self, request, *args, **kwargs):
        try:
            playlist_track = PlaylistTrack.objects.get(id=kwargs['pk'])
            trackData = _build_track(playlist_track)
        except:
            response = {
                'message': 'Playlist track not found',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        return Response(trackData)

    # Removes playlist from db (Cascading)
    def destroy(self, request, *args, **kwargs):
        try:
            playlist_track = PlaylistTrack.objects.get(id=kwargs['pk'])
            playlist_id = playlist_track.playlist.id
            playlist_track.delete()
            _reset_track_positions(playlist_id)
        except:
            response = {
                'message': 'Playlist track not found',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Track removed from playlist'})

    def pre_save(self, obj):
        obj.owner = self.request.user


class PlaylistTrackUpdateOrder(generics.GenericAPIView):
    """
    Update the position of a track in a given playlist
    """
    def get(self, request, *args, **kwargs):
        track_id = kwargs['pk']
        direction = kwargs['direction']

        try:
            track = PlaylistTrack.objects.get(id=track_id)
            new_position = int(track.position) + int(direction)
        except:
            response = {
                'message': 'Playlist track not found',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        try:
            over_riding_track = PlaylistTrack.objects.get(
                playlist_id=track.playlist_id,
                position=new_position
            )
            over_riding_track.position = track.position
            over_riding_track.save()
        except:
            response = {
                'message': 'Could not update track order, level breached',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        track.position = new_position
        track.save()

        return Response({'message': 'track position updated'})
