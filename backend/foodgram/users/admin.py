from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_filter = (
        'username', 'email', 'is_staff', 'is_superuser', 'is_active', 'groups')
