# thrid party imports
from django.contrib import admin

# local imports
from .models import Player


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

admin.site.register(Player, PlayerAdmin)
