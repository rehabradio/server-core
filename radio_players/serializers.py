# third-party imports
from rest_framework import serializers

# local imports
from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    location = serializers.CharField()
    auth_token = serializers.CharField()
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()

    class Meta:
        model = Player
        view_name = 'radio-players-detail'
        fields = ('id', 'name', 'description')
