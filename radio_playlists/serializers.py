# third-party imports
from rest_framework import pagination
from rest_framework import serializers

# local imports
from .models import Playlist, PlaylistTrack
from radio_metadata.serializers import TrackSerializer


class PlaylistSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    owner = serializers.Field(source='owner.username')
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()

    class Meta:
        model = Playlist
        view_name = 'radio-playlists-api-detail'
        fields = ('id', 'name', 'description')


class PlaylistTrackSerializer(serializers.ModelSerializer):
    track = TrackSerializer()
    position = serializers.IntegerField(read_only=True)
    playlist = PlaylistSerializer(write_only=True)
    owner = serializers.Field(source='owner.username')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PlaylistTrack
        fields = ('id', 'position', 'owner', 'track', 'created', 'updated')


class PaginatedPlaylistTrackSerializer(pagination.PaginationSerializer):
    """
    Serializes page objects of playlist track querysets.
    """
    class Meta:
        object_serializer_class = PlaylistTrackSerializer
