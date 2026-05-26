from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Ministry, MinistryMembership
from accounts.models import CustomUser


class MinistryForm(forms.ModelForm):
    class Meta:
        model = Ministry
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.Textarea)):
                field.widget.attrs['class'] = 'form-control'


@login_required
def ministry_list(request):
    ministries = Ministry.objects.prefetch_related('memberships').select_related('leader').all()
    return render(request, 'ministries/ministry_list.html', {'ministries': ministries})


@login_required
def ministry_detail(request, pk):
    ministry = get_object_or_404(Ministry, pk=pk)
    memberships = ministry.memberships.select_related('member').filter(is_active=True)
    return render(request, 'ministries/ministry_detail.html', {'ministry': ministry, 'memberships': memberships})


@login_required
def ministry_create(request):
    if not request.user.is_ministry_leader:
        messages.error(request, 'Access denied.')
        return redirect('ministry_list')
    form = MinistryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Ministry created.')
        return redirect('ministry_list')
    return render(request, 'ministries/ministry_form.html', {'form': form})


@login_required
def ministry_edit(request, pk):
    if not request.user.is_ministry_leader:
        messages.error(request, 'Access denied.')
        return redirect('ministry_list')
    ministry = get_object_or_404(Ministry, pk=pk)
    form = MinistryForm(request.POST or None, instance=ministry)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Ministry updated.')
        return redirect('ministry_detail', pk=ministry.pk)
    return render(request, 'ministries/ministry_form.html', {'form': form, 'ministry': ministry})


@login_required
def add_ministry_member(request, pk):
    ministry = get_object_or_404(Ministry, pk=pk)
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        role = request.POST.get('role', 'member')
        member = get_object_or_404(CustomUser, pk=member_id)
        MinistryMembership.objects.get_or_create(ministry=ministry, member=member, defaults={'role': role})
        messages.success(request, f'{member.get_full_name()} added to {ministry.name}.')
    return redirect('ministry_detail', pk=pk)
