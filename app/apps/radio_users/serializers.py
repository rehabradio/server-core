# Third party imports
from django.contrib.auth.models import User
from rest_framework import pagination
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('avatar',)


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.URLField(source='profile.avatar', read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'avatar',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_superuser',
            'is_staff',
            'last_login',
            'date_joined'
        )


class PaginatedUserSerializer(pagination.PaginationSerializer):
    """
    Serializes page objects of tracks.
    """
    class Meta:
        object_serializer_class = UserSerializer
