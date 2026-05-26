from django.contrib import admin
from .models import ServiceType, AttendanceRecord, AttendanceEntry

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('service_type', 'date', 'get_count', 'recorded_by')
    list_filter = ('service_type',)
    def get_count(self, obj): return obj.get_count()
    get_count.short_description = 'Count'

@admin.register(AttendanceEntry)
class AttendanceEntryAdmin(admin.ModelAdmin):
    list_display = ('record', 'member', 'is_present')
