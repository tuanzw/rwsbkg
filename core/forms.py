from django import forms

from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button

from .models import Carrier

from .validators import validate_alphanumeric


class CarrierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.add_input(Submit('submit', 'Submit'))
    
    class Meta:
        model = Carrier
        fields = ('carrier', 'name', 'address')
        widgets = {
            'carrier': forms.TextInput(attrs={
                'length': 20,
                'placeholder': 'Only alphaNumeric accepted!',
                'hx-get': reverse_lazy('check_carrier'),
                'hx-trigger': 'keyup changed delay:500ms',
                'hx-target': '#div_id_carrier',
                'hx-swap': 'outerHTML',
            }),
            'name': forms.TextInput(attrs={
                'length': 200,
                'placeholder': 'Name'
            }),
            'address': forms.TextInput(attrs={
                'length': 300,
                'placeholder': 'Address'
            }),
        }
    
    def clean_carrier(self):
        inputted_carrier = self.cleaned_data['carrier']
        validate_alphanumeric(inputted_carrier)
        return inputted_carrier
        
        
    def save(self, commit=True):
        carrier = super().save(commit=False)
        if commit:
            carrier.save()
        return carrier
