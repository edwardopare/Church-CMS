"""Ministry management: create ministries, assign leaders, manage members."""
from django.db import models
from accounts.models import CustomUser


class Ministry(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    leader = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_ministries')
    is_active = models.BooleanField(default=True)
    meeting_schedule = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Ministries'
        ordering = ['name']

    def __str__(self):
        return self.name


class MinistryMembership(models.Model):
    ROLES = [('member', 'Member'), ('assistant', 'Assistant Leader'), ('leader', 'Leader')]
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE, related_name='memberships')
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES, default='member')
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('ministry', 'member')

    def __str__(self):
        return f"{self.member.get_full_name()} - {self.ministry.name}"
