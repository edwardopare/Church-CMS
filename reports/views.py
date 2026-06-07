"""Reporting & analytics — membership growth, attendance, finance summaries."""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from members.models import Member, Visitor
from attendance.models import AttendanceEntry
from finance.models import Transaction
from ministries.models import Ministry


@login_required
def reports_dashboard(request):
    if not request.user.is_church_admin and not request.user.is_pastor:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    today = timezone.now().date()
    month_start = today.replace(day=1)

    total_members = Member.objects.count()
    active_members = Member.objects.filter(membership_status='active').count()
    new_this_month = Member.objects.filter(
        membership_date__gte=month_start
    ).count()

    attendance_30 = AttendanceEntry.objects.filter(
        record__date__gte=today - timedelta(days=30),
        is_present=True
    ).count()

    monthly_income = Transaction.objects.filter(
        date__gte=month_start
    ).exclude(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0

    ministry_count = Ministry.objects.filter(is_active=True).count()

    total_visitors = Visitor.objects.count()
    converted = Visitor.objects.filter(status='converted').count()

    # Membership growth last 6 months
    growth = []
    for i in range(5, -1, -1):
        m_start = (today.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
        count = Member.objects.filter(membership_date__lte=m_start).count()
        growth.append({'label': m_start.strftime('%b %Y'), 'count': count})

    return render(request, 'reports/dashboard.html', {
        'total_members': total_members,
        'active_members': active_members,
        'new_this_month': new_this_month,
        'attendance_30': attendance_30,
        'monthly_income': monthly_income,
        'ministry_count': ministry_count,
        'total_visitors': total_visitors,
        'converted_visitors': converted,
        'conversion_rate': round((converted / total_visitors * 100), 1) if total_visitors else 0,
        'growth': growth,
    })
