# third-party imports
from rest_framework import serializers

# local imports
from .models import QueuedTrack


class QueueSerializer(serializers.ModelSerializer):

    class Meta:
        model = QueuedTrack
