# third-party imports
from rest_framework import pagination
from rest_framework import serializers

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
    artists = ArtistSerializer(many=True)
    album = AlbumSerializer(required=False)

    # track metadata
    duration_ms = serializers.IntegerField()
    preview_url = serializers.URLField()
    track_number = serializers.IntegerField()
    image_small = serializers.URLField(required=False)
    image_medium = serializers.URLField(required=False)
    image_large = serializers.URLField(required=False)

    # track stats
    play_count = serializers.IntegerField()
    owner = serializers.Field(source='owner.username')
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()

    class Meta:
        model = Track


class PaginatedTrackSerializer(pagination.PaginationSerializer):
    """
    Serializes page objects of tracks.
    """
    class Meta:
        object_serializer_class = TrackSerializer
