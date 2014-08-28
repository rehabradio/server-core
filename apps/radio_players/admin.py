# thrid party imports
from django.contrib import admin

# local imports
from .models import Player


class PlayerAdmin(admin.ModelAdmin):
    fields = ['name', 'location', 'queue', 'active']
    list_display = (
        'name', 'location', 'token', 'queue', 'active', 'owner', 'created', 'updated')

admin.site.register(Player, PlayerAdmin)
