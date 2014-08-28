# thrid party imports
from django.contrib import admin
from django.core.exceptions import ValidationError

# local imports
from .models import Player


class PlayerAdmin(admin.ModelAdmin):
    fields = ['name', 'location', 'queue', 'active']
    list_display = ('name', 'location', 'token', 'queue', 'active', 'owner', 'created', 'updated')
    #exclude = ['age']

admin.site.register(Player, PlayerAdmin)
