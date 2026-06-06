"""
Member and Visitor forms.
Change 5: All date fields have max_date = today to prevent future date selection.
"""
from django import forms
from django.utils import timezone
from .models import Member, Visitor

today = timezone.now().date().isoformat()  # used as max attr on date inputs


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ('membership_number', 'created_at', 'updated_at')
        widgets = {
            # Change 5: max=today on all date fields
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'max': today, 'class': 'form-control'}),
            'membership_date': forms.DateInput(attrs={'type': 'date', 'max': today, 'class': 'form-control'}),
            'baptism_date': forms.DateInput(attrs={'type': 'date', 'max': today, 'class': 'form-control'}),
            'confirmation_date': forms.DateInput(attrs={'type': 'date', 'max': today, 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            w = field.widget
            if not isinstance(w, (forms.CheckboxInput, forms.Textarea, forms.DateInput)):
                w.attrs.setdefault('class', 'form-control')

    def clean_date_of_birth(self):
        d = self.cleaned_data.get('date_of_birth')
        if d and d > timezone.now().date():
            raise forms.ValidationError('Date of birth cannot be in the future.')
        return d

    def clean_membership_date(self):
        d = self.cleaned_data.get('membership_date')
        if d and d > timezone.now().date():
            raise forms.ValidationError('Membership date cannot be in the future.')
        return d

    def clean_baptism_date(self):
        d = self.cleaned_data.get('baptism_date')
        if d and d > timezone.now().date():
            raise forms.ValidationError('Baptism date cannot be in the future.')
        return d

    def clean_confirmation_date(self):
        d = self.cleaned_data.get('confirmation_date')
        if d and d > timezone.now().date():
            raise forms.ValidationError('Confirmation date cannot be in the future.')
        return d


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = '__all__'
        widgets = {
            # Change 5: max=today on date fields
            'visit_date': forms.DateInput(attrs={'type': 'date', 'max': today, 'class': 'form-control'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'follow_up_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            w = field.widget
            if not isinstance(w, (forms.CheckboxInput, forms.Textarea, forms.DateInput)):
                w.attrs.setdefault('class', 'form-control')

    def clean_visit_date(self):
        d = self.cleaned_data.get('visit_date')
        if d and d > timezone.now().date():
            raise forms.ValidationError('Visit date cannot be in the future.')
        return d
