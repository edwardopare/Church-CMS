"""Attendance tracking for services, small groups, and ministries."""
from django.db import models
from accounts.models import CustomUser


class ServiceType(models.Model):
    name = models.CharField(max_length=100)  # e.g., Sunday Service, Wednesday Bible Study
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AttendanceRecord(models.Model):
    """Tracks a single service/event attendance session."""
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    date = models.DateField()
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='recorded_attendance')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('service_type', 'date')

    def __str__(self):
        return f"{self.service_type} - {self.date}"

    def get_count(self):
        return self.entries.count()


class AttendanceEntry(models.Model):
    """Individual attendance entry per member per service."""
    record = models.ForeignKey(AttendanceRecord, on_delete=models.CASCADE, related_name='entries')
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=True)
    is_first_time = models.BooleanField(default=False)
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('record', 'member')

    def __str__(self):
        return f"{self.member.get_full_name()} - {self.record}"
