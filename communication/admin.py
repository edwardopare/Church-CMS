from django.contrib import admin
from .models import Announcement, Message

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'priority', 'is_published', 'publish_date')
    list_filter = ('priority', 'is_published')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'is_read', 'sent_at')
