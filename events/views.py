from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.utils import timezone
from .models import Event, EventRegistration


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('created_at',)
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.Textarea, forms.DateTimeInput)):
                field.widget.attrs['class'] = 'form-control'


@login_required
def event_list(request):
    upcoming = Event.objects.filter(start_datetime__gte=timezone.now()).order_by('start_datetime')
    past = Event.objects.filter(start_datetime__lt=timezone.now()).order_by('-start_datetime')[:10]
    return render(request, 'events/event_list.html', {'upcoming': upcoming, 'past': past})


@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user_registered = event.registrations.filter(member=request.user, status='confirmed').exists()
    return render(request, 'events/event_detail.html', {'event': event, 'user_registered': user_registered})


@login_required
def event_create(request):
    if not request.user.is_ministry_leader:
        messages.error(request, 'Access denied.')
        return redirect('event_list')
    form = EventForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        event = form.save(commit=False)
        event.organizer = request.user
        event.save()
        messages.success(request, f'Event "{event.title}" created.')
        return redirect('event_detail', pk=event.pk)
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create Event'})


@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not event.requires_registration:
        messages.info(request, 'This event does not require registration.')
        return redirect('event_detail', pk=pk)
    if event.is_full:
        status = 'waitlist'
    else:
        status = 'confirmed'
    reg, created = EventRegistration.objects.get_or_create(
        event=event, member=request.user, defaults={'status': status}
    )
    if created:
        messages.success(request, f'Registered for "{event.title}" ({reg.get_status_display()}).')
    else:
        messages.info(request, 'Already registered.')
    return redirect('event_detail', pk=pk)


@login_required
def event_calendar(request):
    events = Event.objects.filter(start_datetime__gte=timezone.now()).values(
        'id', 'title', 'start_datetime', 'end_datetime', 'event_type'
    )
    import json
    from django.core.serializers.json import DjangoJSONEncoder
    events_json = json.dumps(list(events), cls=DjangoJSONEncoder)
    return render(request, 'events/calendar.html', {'events_json': events_json})
