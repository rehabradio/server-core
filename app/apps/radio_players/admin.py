# std-lib imports
import uuid

# thrid party imports
from django.contrib import admin

# local imports
from .models import Player


class PlayerAdmin(admin.ModelAdmin):
    fields = ['name', 'location', 'queue']
    list_display = (
        'name', 'location', 'token', 'queue',
        'active', 'date_joined', 'last_login', 'owner')

    def save_model(self, request, obj, form, change):
        """Set some initial values when first creating the record.
        """
        if change is False:
            obj.owner = request.user.id
            obj.username = '{0} (Player)'.format(obj.name)
            obj.token = uuid.uuid4()

        obj.save()

admin.site.register(Player, PlayerAdmin)
