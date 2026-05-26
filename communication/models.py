"""Communication: announcements, internal messages."""
from django.db import models
from accounts.models import CustomUser


class Announcement(models.Model):
    PRIORITY = [('low', 'Low'), ('normal', 'Normal'), ('high', 'High'), ('urgent', 'Urgent')]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY, default='normal')
    is_published = models.BooleanField(default=True)
    target_roles = models.CharField(max_length=200, blank=True, help_text='Comma-separated roles or empty for all')
    publish_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Message(models.Model):
    """Internal direct message between users."""
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"From {self.sender} to {self.recipient}: {self.subject}"
