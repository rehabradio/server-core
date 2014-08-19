# third-party imports
from rest_framework import pagination, serializers

# local imports
from .models import Queue, QueueTrack, QueueTrackHistory
from radio_metadata.serializers import TrackSerializer


class QueueSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    owner = serializers.Field(source='owner.username')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Queue


class PaginatedQueueSerializer(pagination.PaginationSerializer):
    """
    Serializes page objects of queue querysets.
    """
    class Meta:
        object_serializer_class = QueueSerializer


class QueueTrackSerializer(serializers.ModelSerializer):
    track = TrackSerializer()
    queue = serializers.PrimaryKeyRelatedField(read_only=True)
    position = serializers.IntegerField(read_only=True)
    owner = serializers.Field(source='owner.username')

    class Meta:
        model = QueueTrack


class PaginatedQueueTrackSerializer(pagination.PaginationSerializer):
    """
    Serializes page objects of queue track querysets.
    """
    class Meta:
        object_serializer_class = QueueTrackSerializer


class QueueTrackHistorySerializer(serializers.ModelSerializer):
    track = TrackSerializer()
    queue = serializers.PrimaryKeyRelatedField(read_only=True)
    owner = serializers.Field(source='owner.username')
    created = serializers.DateTimeField()

    class Meta:
        model = QueueTrackHistory


class PaginatedQueueTrackHistorySerializer(pagination.PaginationSerializer):
    """
    Serializes page objects of queue track history querysets.
    """
    class Meta:
        object_serializer_class = QueueTrackHistorySerializer
