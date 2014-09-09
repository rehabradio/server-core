# third-party imports
from rest_framework import serializers

# local imports
from .models import Player
from radio_queue.serializers import QueueSerializer


class PlayerSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    location = serializers.CharField()
    token = serializers.CharField(write_only=True)
    queue = QueueSerializer()
    active = serializers.BooleanField()
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Player
        view_name = 'radio-players-detail'
