from django.contrib import admin
from .models import Transaction, FundCategory, Pledge

@admin.register(FundCategory)
class FundCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'transaction_type', 'amount', 'member', 'fund_category', 'payment_method')
    list_filter = ('transaction_type', 'payment_method')
    search_fields = ('member__first_name', 'member__last_name')

@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount_pledged', 'amount_paid', 'status')
    list_filter = ('status',)
