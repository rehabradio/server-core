# third-party imports
from rest_framework import serializers

# local imports
from .models import Player
from radio_queue.serializers import QueueSerializer


class PlayerSerializer(serializers.ModelSerializer):
    queue = QueueSerializer()

    class Meta:
        model = Player
        view_name = 'radio-players-detail'
        fields = (
            'id',
            'name',
            'location',
            'queue',
            'active',
            'date_joined',
        )
