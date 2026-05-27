"""Context processors to add global variables to templates."""
from communication.models import Message, Announcement


def notifications(request):
    """Add unread message and announcement counts to all templates."""
    if not request.user.is_authenticated:
        return {
            'unread_messages_count': 0,
            'unread_announcements_count': 0,
        }
    
    unread_messages = Message.objects.filter(
        recipient=request.user, 
        is_read=False
    ).count()
    
    # Get unread announcements (announcements published after user's last visit)
    unread_announcements = Announcement.objects.filter(
        is_published=True
    ).exclude(
        target_roles__icontains=request.user.get_role_display()
    ) if request.user.get_role_display() else Announcement.objects.filter(is_published=True).count()
    
    # Simplified: count all published announcements for now
    unread_announcements = Announcement.objects.filter(is_published=True).count()
    
    return {
        'unread_messages_count': unread_messages,
        'unread_announcements_count': unread_announcements,
    }
