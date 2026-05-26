from django.contrib import admin
from .models import Event, EventRegistration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'start_datetime', 'location', 'organizer')
    list_filter = ('event_type',)
    search_fields = ('title',)

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'member', 'status', 'registered_at')
