"""
Member Management models.
Members are stored directly (no system user account required).
"""
from django.db import models
from accounts.models import CustomUser


class Member(models.Model):
    """Church member stored as a standalone record — no system login required."""
    MEMBERSHIP_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('transferred', 'Transferred'),
        ('deceased', 'Deceased'),
        ('suspended', 'Suspended'),
    ]
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    # Personal info directly on the member (no linked user account)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    profile_photo = models.ImageField(upload_to='members/', blank=True, null=True)

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
        ordering = ['last_name', 'first_name']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.get_full_name()} - {self.membership_number}"

    def save(self, *args, **kwargs):
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
    # Change 8: plain text instead of FK to Member/User
    converted_member_name = models.CharField(
        max_length=200, blank=True,
        help_text='If converted, enter the member name'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-visit_date']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.visit_date}"
