from django import forms
from django.utils import timezone
from .models import AttendanceRecord, ServiceType

today = timezone.now().date().isoformat()


class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ('service_type', 'date', 'notes')
        widgets = {
            # Change 5: attendance date cannot be in the future
            'date': forms.DateInput(attrs={'type': 'date', 'max': today, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_type'].widget.attrs['class'] = 'form-control'

    def clean_date(self):
        d = self.cleaned_data.get('date')
        if d and d > timezone.now().date():
            raise forms.ValidationError('Attendance date cannot be in the future.')
        return d


class ServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
