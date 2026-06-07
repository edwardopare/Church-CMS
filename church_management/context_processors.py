"""Context processors — inject notification counts into every template."""
from communication.models import Message, Announcement


def notifications(request):
    """Add unread counts to all template contexts."""
    if not request.user.is_authenticated:
        return {
            'unread_messages_count': 0,
            'unread_announcements_count': 0,
        }
    return {
        'unread_messages_count': Message.objects.filter(
            recipient=request.user, is_read=False
        ).count(),
        'unread_announcements_count': Announcement.objects.filter(
            is_published=True
        ).count(),
    }
