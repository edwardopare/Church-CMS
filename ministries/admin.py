from django.contrib import admin
from .models import Ministry, MinistryMembership

@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'is_active')
    list_filter = ('is_active',)

@admin.register(MinistryMembership)
class MinistryMembershipAdmin(admin.ModelAdmin):
    list_display = ('ministry', 'member', 'role', 'is_active')
