from django.contrib import admin
from .models import Member, Visitor

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('membership_number', 'get_full_name', 'membership_status', 'is_baptised')
    list_filter = ('membership_status', 'is_baptised', 'is_confirmed', 'gender')
    search_fields = ('first_name', 'last_name', 'membership_number', 'email')

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Name'

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'visit_date', 'status', 'assigned_to')
    list_filter = ('status',)
    search_fields = ('first_name', 'last_name', 'email')