import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from django.http import HttpResponse
from datetime import timedelta
from .models import Transaction, FundCategory
from .forms import TransactionForm, FundCategoryForm


def finance_required(view_func):
    """Decorator: restrict view to finance officers and admins."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.conf import settings
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        if not request.user.is_finance:
            messages.error(request, 'Access denied. Finance role required.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@login_required
def finance_dashboard(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    monthly_income = Transaction.objects.filter(
        date__gte=month_start, date__lte=today
    ).exclude(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0

    monthly_expenses = Transaction.objects.filter(
        date__gte=month_start, date__lte=today,
        transaction_type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0

    year_start = today.replace(month=1, day=1)
    annual_income = Transaction.objects.filter(
        date__gte=year_start
    ).exclude(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0

    recent = Transaction.objects.select_related('member', 'fund_category').order_by('-date')[:10]
    by_category = FundCategory.objects.annotate(
        total=Sum('transaction__amount', filter=Q(transaction__date__gte=month_start))
    ).values('name', 'total')

    return render(request, 'finance/dashboard.html', {
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'annual_income': annual_income,
        'net_monthly': monthly_income - monthly_expenses,
        'recent': recent,
        'by_category': list(by_category),
    })


@finance_required
def transaction_list(request):
    transactions = Transaction.objects.select_related('member', 'fund_category').all()
    t_type = request.GET.get('type')
    if t_type:
        transactions = transactions.filter(transaction_type=t_type)
    return render(request, 'finance/transaction_list.html', {
        'transactions': transactions,
        'transaction_types': Transaction.TRANSACTION_TYPES,
        'selected_type': t_type,
    })


@finance_required
def transaction_create(request):
    form = TransactionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        t = form.save(commit=False)
        t.recorded_by = request.user
        t.save()
        messages.success(request, f'Transaction recorded: {t.get_transaction_type_display()} — GHS {t.amount}')
        return redirect('transaction_list')
    return render(request, 'finance/transaction_form.html', {'form': form, 'title': 'Record Transaction'})


@finance_required
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(request, 'finance/transaction_detail.html', {'transaction': transaction})


@login_required
def financial_report(request):
    if not request.user.is_finance:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    today = timezone.now().date()
    months = _build_monthly_data(today)
    return render(request, 'finance/report.html', {'months': months})


@login_required
def financial_report_download(request):
    """Download financial report as CSV."""
    if not request.user.is_finance:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    today = timezone.now().date()
    months = _build_monthly_data(today)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="financial_report_{today}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Church of Christ - RedTop Financial Report'])
    writer.writerow([f'Generated: {today.strftime("%B %d, %Y")}'])
    writer.writerow([])
    writer.writerow(['Month', 'Income (GHS)', 'Expenses (GHS)', 'Net (GHS)'])

    total_income = total_expense = 0
    for m in months:
        writer.writerow([m['label'], f"{m['income']:.2f}", f"{m['expense']:.2f}", f"{m['net']:.2f}"])
        total_income += m['income']
        total_expense += m['expense']

    writer.writerow([])
    writer.writerow(['TOTALS', f"{total_income:.2f}", f"{total_expense:.2f}", f"{(total_income - total_expense):.2f}"])

    # Transaction detail
    writer.writerow([])
    writer.writerow(['--- Transaction Detail (Last 12 Months) ---'])
    writer.writerow(['Date', 'Type', 'Member', 'Fund', 'Amount (GHS)', 'Method'])

    year_ago = today - timedelta(days=365)
    txns = Transaction.objects.filter(date__gte=year_ago).select_related('member', 'fund_category').order_by('-date')
    for t in txns:
        member_name = 'Anonymous' if t.anonymous else (t.member.get_full_name() if t.member else '—')
        writer.writerow([
            t.date.strftime('%Y-%m-%d'),
            t.get_transaction_type_display(),
            member_name,
            t.fund_category.name if t.fund_category else '—',
            f"{t.amount:.2f}",
            t.get_payment_method_display(),
        ])

    return response


def _build_monthly_data(today):
    """Build last 12 months income/expense summary."""
    months = []
    for i in range(11, -1, -1):
        m_start = (today.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
        if m_start.month == 12:
            m_end = m_start.replace(year=m_start.year + 1, month=1, day=1)
        else:
            m_end = m_start.replace(month=m_start.month + 1, day=1)
        income = Transaction.objects.filter(
            date__gte=m_start, date__lt=m_end
        ).exclude(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0
        expense = Transaction.objects.filter(
            date__gte=m_start, date__lt=m_end,
            transaction_type='expense'
        ).aggregate(total=Sum('amount'))['total'] or 0
        months.append({
            'label': m_start.strftime('%b %Y'),
            'income': float(income),
            'expense': float(expense),
            'net': float(income - expense),
        })
    return months
