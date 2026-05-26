"""Main URL configuration for Church Management System."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.utils import timezone


@login_required
def dashboard(request):
    """Main dashboard — aggregates key metrics for the logged-in user."""
    from accounts.models import CustomUser
    from members.models import Member, Visitor
    from events.models import Event
    from attendance.models import AttendanceEntry, AttendanceRecord
    from finance.models import Transaction
    from communication.models import Announcement, Message
    from datetime import timedelta, date

    today = timezone.now().date()
    month_start = today.replace(day=1)

    ctx = {
        'total_members': Member.objects.count(),
        'active_members': Member.objects.filter(membership_status='active').count(),
        'upcoming_events': Event.objects.filter(start_datetime__gte=timezone.now()).order_by('start_datetime')[:5],
        'announcements': Announcement.objects.filter(is_published=True).order_by('-created_at')[:5],
        'unread_messages': Message.objects.filter(recipient=request.user, is_read=False).count(),
    }

    if request.user.is_finance:
        ctx['monthly_income'] = Transaction.objects.filter(
            date__gte=month_start
        ).exclude(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0

    if request.user.is_church_admin or request.user.is_pastor:
        # Attendance trend last 4 weeks
        weeks = []
        for i in range(3, -1, -1):
            w_start = today - timedelta(weeks=i+1)
            w_end = today - timedelta(weeks=i)
            cnt = AttendanceEntry.objects.filter(
                record__date__gte=w_start,
                record__date__lt=w_end,
                is_present=True
            ).count()
            weeks.append({'label': w_start.strftime('%b %d'), 'count': cnt})
        ctx['attendance_weeks'] = weeks
        ctx['new_visitors'] = Visitor.objects.filter(
            visit_date__gte=month_start
        ).count()

    return render(request, 'dashboard.html', ctx)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda req: redirect('dashboard')),
    path('dashboard/', dashboard, name='dashboard'),
    path('accounts/', include('accounts.urls')),
    path('members/', include('members.urls')),
    path('attendance/', include('attendance.urls')),
    path('finance/', include('finance.urls')),
    path('ministries/', include('ministries.urls')),
    path('events/', include('events.urls')),
    path('communications/', include('communication.urls')),
    path('reports/', include('reports.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
