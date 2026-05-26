"""Accounts views: registration, login, logout, profile, user management."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import JsonResponse
from .models import CustomUser
from .forms import RegisterForm, LoginForm, ProfileUpdateForm, UserManagementForm


def register_view(request):
    form = RegisterForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.role = 'member'  # default role
        user.save()
        login(request, user)
        messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
        return redirect('dashboard')
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, f'Welcome back, {form.get_user().first_name}!')
        return redirect(request.GET.get('next', 'dashboard'))
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def profile_view(request):
    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def change_password_view(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Password changed successfully.')
        return redirect('profile')
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def user_list_view(request):
    """Admin view: list all users."""
    if not request.user.is_church_admin:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    users = CustomUser.objects.all().order_by('role', 'last_name')
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
def user_edit_view(request, pk):
    """Admin view: edit a user's role and info."""
    if not request.user.is_church_admin:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    user = get_object_or_404(CustomUser, pk=pk)
    form = UserManagementForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'User {user.get_full_name()} updated.')
        return redirect('user_list')
    return render(request, 'accounts/user_edit.html', {'form': form, 'target_user': user})
