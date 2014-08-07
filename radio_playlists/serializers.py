# third-party imports
from rest_framework import serializers

# local imports
from .models import Playlist, PlaylistTrack


class PlaylistSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Playlist
        view_name = 'radio-playlists-api-detail'
        fields = ('id', 'name', 'description')


class PlaylistTrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlaylistTrack
