from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Announcement, Message
from accounts.models import CustomUser


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        exclude = ('author', 'created_at', 'publish_date')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.Textarea, forms.DateInput)):
                field.widget.attrs['class'] = 'form-control'


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('recipient', 'subject', 'body')
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'form-control'


@login_required
def announcement_list(request):
    announcements = Announcement.objects.filter(is_published=True).select_related('author')
    return render(request, 'communication/announcement_list.html', {'announcements': announcements})


@login_required
def announcement_create(request):
    if not request.user.is_church_admin and not request.user.is_pastor:
        messages.error(request, 'Access denied.')
        return redirect('announcement_list')
    form = AnnouncementForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        ann = form.save(commit=False)
        ann.author = request.user
        ann.save()
        messages.success(request, 'Announcement published.')
        return redirect('announcement_list')
    return render(request, 'communication/announcement_form.html', {'form': form})


@login_required
def inbox(request):
    received = Message.objects.filter(recipient=request.user).select_related('sender')
    unread_count = received.filter(is_read=False).count()
    return render(request, 'communication/inbox.html', {'messages_list': received, 'unread_count': unread_count})


@login_required
def send_message(request):
    form = MessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        msg = form.save(commit=False)
        msg.sender = request.user
        msg.save()
        messages.success(request, f'Message sent to {msg.recipient.get_full_name()}.')
        return redirect('inbox')
    return render(request, 'communication/send_message.html', {'form': form})


@login_required
def message_detail(request, pk):
    msg = get_object_or_404(Message, pk=pk, recipient=request.user)
    msg.is_read = True
    msg.save()
    return render(request, 'communication/message_detail.html', {'msg': msg})
