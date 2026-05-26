"""
Finance module: tithes, offerings, donations, pledges, expenses.
Generates receipts and financial reports.
"""
from django.db import models
from accounts.models import CustomUser
import uuid


class FundCategory(models.Model):
    """Named fund category, e.g. Building Fund, Missions, General."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Fund Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """Core financial transaction (income or expense)."""
    TRANSACTION_TYPES = [
        ('tithe', 'Tithe'),
        ('offering', 'Offering'),
        ('donation', 'Donation'),
        ('pledge_payment', 'Pledge Payment'),
        ('expense', 'Expense'),
        ('other_income', 'Other Income'),
    ]
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
        ('card', 'Card'),
        ('online', 'Online'),
    ]

    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    member = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    anonymous = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    fund_category = models.ForeignKey(FundCategory, on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    date = models.DateField()
    description = models.TextField(blank=True)
    receipt_issued = models.BooleanField(default=False)
    recorded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='recorded_transactions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} ({self.date})"

    @property
    def is_income(self):
        return self.transaction_type != 'expense'


class Pledge(models.Model):
    """Member pledge commitments with payment tracking."""
    STATUS = [
        ('active', 'Active'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
    ]

    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fund_category = models.ForeignKey(FundCategory, on_delete=models.SET_NULL, null=True)
    amount_pledged = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS, default='active')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.get_full_name()} - {self.amount_pledged}"

    @property
    def balance(self):
        return self.amount_pledged - self.amount_paid

    @property
    def completion_percentage(self):
        if self.amount_pledged == 0:
            return 0
        return round((self.amount_paid / self.amount_pledged) * 100, 1)
