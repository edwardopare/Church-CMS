from django.contrib import admin
from .models import Member, Family, Visitor

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('membership_number', 'get_name', 'membership_status', 'family', 'is_baptised')
    list_filter = ('membership_status', 'is_baptised', 'is_confirmed')
    search_fields = ('user__first_name', 'user__last_name', 'membership_number')

    def get_name(self, obj):
        return obj.user.get_full_name()
    get_name.short_description = 'Name'

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_member_count')
    def get_member_count(self, obj):
        return obj.members.count()
    get_member_count.short_description = 'Members'

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'visit_date', 'status', 'assigned_to')
    list_filter = ('status',)
    search_fields = ('first_name', 'last_name', 'email')
