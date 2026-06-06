from django import forms
from django.utils import timezone
from .models import Transaction, FundCategory

today = timezone.now().date().isoformat()


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ('reference', 'created_at', 'recorded_by')
        widgets = {
            # Change 5: transaction date cannot be future
            'date': forms.DateInput(attrs={'type': 'date', 'max': today, 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.Textarea, forms.DateInput)):
                field.widget.attrs.setdefault('class', 'form-control')

    def clean_date(self):
        d = self.cleaned_data.get('date')
        if d and d > timezone.now().date():
            raise forms.ValidationError('Transaction date cannot be in the future.')
        return d


class FundCategoryForm(forms.ModelForm):
    class Meta:
        model = FundCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'
