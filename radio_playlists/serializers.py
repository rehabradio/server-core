# third-party imports
from rest_framework import serializers

# local imports
from .models import Playlist, PlaylistTrack


class PlaylistSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    owner = serializers.Field(source='owner.username')

    class Meta:
        model = Playlist
        view_name = 'radio-playlists-api-detail'
        fields = ('id', 'name', 'description')


class PlaylistTrackSerializer(serializers.ModelSerializer):
    # playlist to which this track has been added
    #position = serializers.IntegerField()
    owner = serializers.Field(source='owner.username')

    class Meta:
        model = PlaylistTrack
        fields = ('id', 'track', 'playlist', 'position')
