from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Member, Visitor
from .forms import MemberForm, VisitorForm


@login_required
def member_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    members = Member.objects.all()
    if query:
        members = members.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(membership_number__icontains=query) |
            Q(email__icontains=query)
        )
    if status:
        members = members.filter(membership_status=status)
    return render(request, 'members/member_list.html', {
        'members': members, 'query': query, 'status': status,
        'total': members.count(),
    })


@login_required
def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    return render(request, 'members/member_detail.html', {'member': member})


@login_required
def member_create(request):
    if not request.user.can_manage_members:
        messages.error(request, 'Access denied.')
        return redirect('member_list')
    form = MemberForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        member = form.save()
        messages.success(request, f'Member {member.get_full_name()} added successfully.')
        return redirect('member_detail', pk=member.pk)
    return render(request, 'members/member_form.html', {'form': form, 'title': 'Add Member'})


@login_required
def member_edit(request, pk):
    if not request.user.can_manage_members:
        messages.error(request, 'Access denied.')
        return redirect('member_list')
    member = get_object_or_404(Member, pk=pk)
    form = MemberForm(request.POST or None, request.FILES or None, instance=member)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Member updated successfully.')
        return redirect('member_detail', pk=member.pk)
    return render(request, 'members/member_form.html', {'form': form, 'title': 'Edit Member', 'member': member})


@login_required
def member_delete(request, pk):
    if not request.user.is_church_admin:
        messages.error(request, 'Access denied.')
        return redirect('member_list')
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        name = member.get_full_name()
        member.delete()
        messages.success(request, f'Member {name} removed.')
        return redirect('member_list')
    return render(request, 'members/member_confirm_delete.html', {'member': member})


@login_required
def visitor_list(request):
    visitors = Visitor.objects.select_related('assigned_to').all()
    return render(request, 'members/visitor_list.html', {'visitors': visitors})


@login_required
def visitor_create(request):
    form = VisitorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Visitor recorded successfully.')
        return redirect('visitor_list')
    return render(request, 'members/visitor_form.html', {'form': form})


@login_required
def visitor_edit(request, pk):
    visitor = get_object_or_404(Visitor, pk=pk)
    form = VisitorForm(request.POST or None, instance=visitor)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Visitor updated.')
        return redirect('visitor_list')
    return render(request, 'members/visitor_form.html', {'form': form, 'visitor': visitor})