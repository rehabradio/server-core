# third-party imports
from rest_framework import serializers

# local imports
from .models import Player
from radio_queue.serializers import QueueSerializer


class PlayerSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    location = serializers.CharField()
    auth_token = serializers.CharField()
    queue = serializers.PrimaryKeyRelatedField(required=False)
    active = serializers.BooleanField()
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Player
        view_name = 'radio-players-detail'
