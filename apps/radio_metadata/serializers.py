# third-party imports
from rest_framework import pagination
from rest_framework import serializers

# local imports
from .models import Album, Artist, Track


class BaseSerializer(serializers.ModelSerializer):

    source_type = serializers.CharField()
    source_id = serializers.CharField()
    name = serializers.CharField()


class ArtistSerializer(BaseSerializer):

    class Meta:
        model = Artist


class AlbumSerializer(BaseSerializer):

    class Meta:
        model = Album


class TrackSerializer(BaseSerializer):
    # relationships to other models
    artists = ArtistSerializer(many=True, read_only=True)
    album = AlbumSerializer(read_only=True)

    # track metadata
    name = serializers.CharField(read_only=True)
    duration_ms = serializers.IntegerField(read_only=True)
    preview_url = serializers.URLField(read_only=True)
    track_number = serializers.IntegerField(read_only=True)
    image_small = serializers.URLField(read_only=True)
    image_medium = serializers.URLField(read_only=True)
    image_large = serializers.URLField(read_only=True)

    # Additional information
    play_count = serializers.IntegerField(read_only=True)
    owner = serializers.Field(source='owner.username')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Track
        fields = (
            'id',
            'source_type',
            'source_id',
            'name',
            'artists',
            'album',
            'duration_ms',
            'preview_url',
            'track_number',
            'image_small',
            'image_medium',
            'image_large',
            'play_count',
            'owner',
            'created',
            'updated',
        )


class PaginatedTrackSerializer(pagination.PaginationSerializer):
    """Serializes page objects of tracks."""
    class Meta:
        object_serializer_class = TrackSerializer
