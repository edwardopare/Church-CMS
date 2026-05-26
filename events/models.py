"""Events: church services, conferences, special events, registrations."""
from django.db import models
from accounts.models import CustomUser


class Event(models.Model):
    EVENT_TYPES = [
        ('service', 'Regular Service'),
        ('conference', 'Conference'),
        ('outreach', 'Outreach'),
        ('youth', 'Youth Event'),
        ('fundraiser', 'Fundraiser'),
        ('social', 'Social Event'),
        ('training', 'Training / Workshop'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='service')
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    organizer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    max_capacity = models.IntegerField(null=True, blank=True)
    is_public = models.BooleanField(default=True)
    requires_registration = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_datetime']

    def __str__(self):
        return f"{self.title} ({self.start_datetime.strftime('%b %d, %Y')})"

    @property
    def registration_count(self):
        return self.registrations.filter(status='confirmed').count()

    @property
    def is_full(self):
        if not self.max_capacity:
            return False
        return self.registration_count >= self.max_capacity


class EventRegistration(models.Model):
    STATUS = [('confirmed', 'Confirmed'), ('waitlist', 'Waitlist'), ('cancelled', 'Cancelled')]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS, default='confirmed')
    registered_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('event', 'member')

    def __str__(self):
        return f"{self.member.get_full_name()} - {self.event.title}"
