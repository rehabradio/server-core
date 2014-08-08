# third-party imports
from rest_framework import serializers

# local imports
from .models import Playlist, PlaylistTrack
from radio_metadata.serializers import TrackSerializer


class PlaylistSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    owner = serializers.Field(source='owner.username')

    class Meta:
        model = Playlist
        view_name = 'radio-playlists-api-detail'
        fields = ('id', 'name', 'description')


class PlaylistTrackSerializer(serializers.ModelSerializer):
    track = TrackSerializer()
    position = serializers.IntegerField()
    playlist = PlaylistSerializer(write_only=True)
    owner = serializers.Field(source='owner.username')

    class Meta:
        model = PlaylistTrack
        fields = ('id', 'position', 'owner', 'track')
