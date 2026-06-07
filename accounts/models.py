"""
Custom User model with role-based access control.
Extends Django's AbstractUser to add church-specific roles and profile data.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Extended user model with church roles and profile information."""
    
    # Role choices — drives permissions across the system
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('church_admin', 'Church Administrator'),
        ('pastor', 'Pastor / Clergy'),
        ('finance_officer', 'Finance Officer'),
        ('ministry_leader', 'Ministry Leader'),
        ('member', 'Church Member'),
        ('guest', 'Guest / Visitor'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)
    is_active_member = models.BooleanField(default=True)
    join_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    def save(self, *args, **kwargs):
        # Auto-set role based on superuser status
        if self.is_superuser:
            self.role = 'super_admin'
        elif self.is_staff and self.role == 'member':
            # Staff members who aren't superuser get church_admin by default
            self.role = 'church_admin'
        super().save(*args, **kwargs)

    # --- Permission helpers used across templates and views ---

    @property
    def is_super_admin(self):
        return self.role == 'super_admin'

    @property
    def is_church_admin(self):
        return self.role in ('super_admin', 'church_admin')

    @property
    def is_pastor(self):
        return self.role in ('super_admin', 'church_admin', 'pastor')

    @property
    def is_finance(self):
        return self.role in ('super_admin', 'church_admin', 'finance_officer')

    @property
    def is_ministry_leader(self):
        return self.role in ('super_admin', 'church_admin', 'pastor', 'ministry_leader')

    @property
    def can_manage_members(self):
        return self.role in ('super_admin', 'church_admin', 'pastor')
