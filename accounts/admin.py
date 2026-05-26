from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active_member')
    list_filter = ('role', 'is_active_member', 'gender')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        ('Church Info', {'fields': ('role', 'phone', 'address', 'date_of_birth', 'gender',
                                    'profile_photo', 'is_active_member', 'join_date', 'notes')}),
    )
