"""
Member Management models.
Handles family groups, baptism/confirmation records, and membership tracking.
"""
from django.db import models
from accounts.models import CustomUser


class Family(models.Model):
    """Groups members into a family unit."""
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Families'
        ordering = ['name']

    def __str__(self):
        return self.name


class Member(models.Model):
    """Extended profile for church members, linked to a CustomUser."""
    MEMBERSHIP_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('transferred', 'Transferred'),
        ('deceased', 'Deceased'),
        ('suspended', 'Suspended'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='member_profile')
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    membership_number = models.CharField(max_length=20, unique=True, blank=True)
    membership_status = models.CharField(max_length=20, choices=MEMBERSHIP_STATUS, default='active')
    membership_date = models.DateField(null=True, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    is_baptised = models.BooleanField(default=False)
    baptism_date = models.DateField(null=True, blank=True)
    baptism_church = models.CharField(max_length=200, blank=True)
    is_confirmed = models.BooleanField(default=False)
    confirmation_date = models.DateField(null=True, blank=True)
    previous_church = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.membership_number}"

    def save(self, *args, **kwargs):
        # Auto-generate membership number if not set
        if not self.membership_number:
            last = Member.objects.order_by('-id').first()
            next_id = (last.id + 1) if last else 1
            self.membership_number = f"MBR-{next_id:05d}"
        super().save(*args, **kwargs)


class Visitor(models.Model):
    """Track first-time and returning visitors for follow-up."""
    VISIT_STATUS = [
        ('new', 'New Visitor'),
        ('returning', 'Returning Visitor'),
        ('interested', 'Interested in Membership'),
        ('converted', 'Converted to Member'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    visit_date = models.DateField()
    how_heard = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=VISIT_STATUS, default='new')
    follow_up_date = models.DateField(null=True, blank=True)
    follow_up_notes = models.TextField(blank=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    converted_member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-visit_date']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.visit_date}"
