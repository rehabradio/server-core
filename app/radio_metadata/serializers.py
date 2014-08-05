# third-party imports
from rest_framework import pagination
from rest_framework import serializers


class BaseSerializer(serializers.Serializer):

    source_type = serializers.CharField()
    source_id = serializers.CharField()

    name = serializers.CharField()


class ArtistSerializer(BaseSerializer):

    pass


class AlbumSerializer(BaseSerializer):

    pass


class TrackSerializer(BaseSerializer):

    # relationships to other models
    artists = ArtistSerializer(many=True)
    album = AlbumSerializer(required=False)
    owner = serializers.Field(source='owner.username')

    # track metadata
    duration_ms = serializers.IntegerField()
    preview_url = serializers.URLField()
    track_number = serializers.IntegerField()
    image_small = serializers.URLField()
    image_medium = serializers.URLField()
    image_large = serializers.URLField()

    # track stats
    play_count = serializers.IntegerField()
    vote_count = serializers.IntegerField()
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()


class PaginatedTrackSerializer(pagination.PaginationSerializer):
    """
    Serializes page objects of tracks.
    """
    class Meta:
        object_serializer_class = TrackSerializer
