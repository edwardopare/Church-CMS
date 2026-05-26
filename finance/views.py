from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta, date
from .models import Transaction, FundCategory, Pledge
from .forms import TransactionForm, PledgeForm, FundCategoryForm


def finance_required(view_func):
    """Decorator: restrict to finance officers and admins."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_finance:
            messages.error(request, 'Access denied. Finance role required.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return login_required(wrapper)


@login_required
def finance_dashboard(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    # Monthly totals
    monthly_income = Transaction.objects.filter(
        date__gte=month_start, date__lte=today
    ).exclude(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0

    monthly_expenses = Transaction.objects.filter(
        date__gte=month_start, date__lte=today,
        transaction_type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Annual totals
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
    # Filters
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


@finance_required
def pledge_list(request):
    pledges = Pledge.objects.select_related('member', 'fund_category').all()
    return render(request, 'finance/pledge_list.html', {'pledges': pledges})


@finance_required
def pledge_create(request):
    form = PledgeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Pledge recorded.')
        return redirect('pledge_list')
    return render(request, 'finance/pledge_form.html', {'form': form})


@login_required
def financial_report(request):
    if not request.user.is_finance:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    today = timezone.now().date()
    # Last 12 months monthly summaries
    months = []
    for i in range(11, -1, -1):
        # approximate month start
        m_date = today.replace(day=1) - timedelta(days=i * 30)
        m_start = m_date.replace(day=1)
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

    return render(request, 'finance/report.html', {'months': months})
