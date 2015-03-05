# third-party imports
from rest_framework import pagination, serializers

# local imports
from .models import Playlist, PlaylistTrack
from radio_metadata.serializers import TrackSerializer


PROTECTION_OPTIONS = [
    ('private', 'Private'),
    ('public', 'Public'),
]


class PlaylistSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    protection = serializers.ChoiceField(
        choices=PROTECTION_OPTIONS, default='private')
    owner = serializers.Field(source='owner.username')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Playlist
        view_name = 'radio-playlists-api-list'


class PaginatedPlaylistSerializer(pagination.PaginationSerializer):
    """Serializes page objects of playlist querysets."""
    class Meta:
        object_serializer_class = PlaylistSerializer


class PlaylistTrackSerializer(serializers.ModelSerializer):
    track = TrackSerializer()
    position = serializers.IntegerField(read_only=True)
    playlist = serializers.PrimaryKeyRelatedField(read_only=True)
    owner = serializers.Field(source='owner.username')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PlaylistTrack
        view_name = 'radio-playlists-api-detail'


class PaginatedPlaylistTrackSerializer(pagination.PaginationSerializer):
    """Serializes page objects of playlist track querysets."""
    class Meta:
        object_serializer_class = PlaylistTrackSerializer
