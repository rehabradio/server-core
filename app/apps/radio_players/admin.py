# thrid party imports
from django.contrib import admin
from django.core.cache import cache

# local imports
from .models import Player
from radio.utils.cache import build_key


class PlayerAdmin(admin.ModelAdmin):
    fields = ['name', 'location', 'queue', 'active']
    list_display = (
        'name', 'location', 'token', 'queue',
        'active', 'date_joined', 'last_login', 'owner')

    def save_model(self, request, obj, form, change):
        """Set the record owner as the current logged in user,
        when creating a record.
        """
        if change is False:
            obj.owner = request.user.id

        obj.save()

        cache.set(build_key('player', obj.id), obj)

admin.site.register(Player, PlayerAdmin)
