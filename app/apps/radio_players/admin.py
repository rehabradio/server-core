# thrid party imports
from django.contrib import admin

# local imports
from .models import Player


class PlayerAdmin(admin.ModelAdmin):
    fields = ['name', 'location', 'queue', 'active']
    list_display = (
        'name', 'location', 'token', 'queue',
        'active', 'date_joined', 'last_login')

admin.site.register(Player, PlayerAdmin)
