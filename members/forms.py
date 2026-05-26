from django import forms
from .models import Member, Family, Visitor
from accounts.models import CustomUser


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ('membership_number', 'created_at', 'updated_at')
        widgets = {
            'membership_date': forms.DateInput(attrs={'type': 'date'}),
            'baptism_date': forms.DateInput(attrs={'type': 'date'}),
            'confirmation_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = '__all__'
        widgets = {'notes': forms.Textarea(attrs={'rows': 3}), 'address': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = '__all__'
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'follow_up_notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
