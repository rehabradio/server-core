# thrid party imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class UserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_active', 'date_joined', 'is_staff')

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        return qs.exclude(profile__isnull=True)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
