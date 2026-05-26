from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import AttendanceRecord, AttendanceEntry, ServiceType
from .forms import AttendanceRecordForm, ServiceTypeForm
from accounts.models import CustomUser


@login_required
def attendance_list(request):
    records = AttendanceRecord.objects.select_related('service_type', 'recorded_by').annotate(
        count=Count('entries')
    ).order_by('-date')[:50]
    return render(request, 'attendance/attendance_list.html', {'records': records})


@login_required
def attendance_create(request):
    form = AttendanceRecordForm(request.POST or None)
    members = CustomUser.objects.filter(is_active_member=True).order_by('last_name')
    if request.method == 'POST' and form.is_valid():
        record = form.save(commit=False)
        record.recorded_by = request.user
        record.save()
        # Process attendance entries from checkboxes
        for member in members:
            is_present = request.POST.get(f'member_{member.id}') == 'on'
            if is_present:
                AttendanceEntry.objects.get_or_create(
                    record=record, member=member,
                    defaults={'is_present': True}
                )
        messages.success(request, f'Attendance recorded for {record.service_type} on {record.date}.')
        return redirect('attendance_list')
    return render(request, 'attendance/attendance_form.html', {'form': form, 'members': members})


@login_required
def attendance_detail(request, pk):
    record = get_object_or_404(AttendanceRecord, pk=pk)
    entries = record.entries.select_related('member').all()
    return render(request, 'attendance/attendance_detail.html', {'record': record, 'entries': entries})


@login_required
def attendance_analytics(request):
    """Dashboard-level analytics for attendance trends."""
    # Last 8 weeks of attendance data
    weeks = []
    today = timezone.now().date()
    for i in range(7, -1, -1):
        week_start = today - timedelta(weeks=i+1)
        week_end = today - timedelta(weeks=i)
        count = AttendanceEntry.objects.filter(
            record__date__gte=week_start,
            record__date__lt=week_end,
            is_present=True
        ).count()
        weeks.append({'label': week_start.strftime('%b %d'), 'count': count})

    service_stats = ServiceType.objects.annotate(
        total_sessions=Count('attendancerecord'),
    ).values('name', 'total_sessions')

    return render(request, 'attendance/analytics.html', {
        'weeks': weeks,
        'service_stats': list(service_stats),
    })
