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

    duration_ms = serializers.IntegerField(read_only=True)
    preview_url = serializers.URLField(read_only=True)
    play_count = serializers.IntegerField(read_only=True)
    owner = serializers.Field(source='owner.username')
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'avatar',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'is_superuser',
            'is_staff',
            'last_login',
            'date_joined'
        )
        write_only_fields = ('password',)

    def restore_object(self, attrs, instance=None):
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.username = attrs['username'].lower()
        user.set_password(attrs['password'])

        return user


class PaginatedUserSerializer(pagination.PaginationSerializer):
    """
    Serializes page objects of tracks.
    """
    class Meta:
        object_serializer_class = UserSerializer
