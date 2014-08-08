# third-party imports
from rest_framework import serializers

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


class QueueTrackSerializer(serializers.ModelSerializer):
    track = TrackSerializer()
    position = serializers.IntegerField()
    owner = serializers.Field(source='owner.username')

    class Meta:
        model = QueueTrack


class QueueTrackHistorySerializer(serializers.ModelSerializer):
    track = TrackSerializer()
    queue = QueueSerializer()
    owner = serializers.Field(source='owner.username')
    created = serializers.DateTimeField()

    class Meta:
        model = QueueTrackHistory
