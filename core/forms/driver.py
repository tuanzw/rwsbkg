from django import forms
from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper

from ..models import Driver, Carrier

from datetime import datetime
    
class DriverForm(forms.ModelForm):
    fullname = forms.CharField(
        label='Full Name',
        widget=forms.TextInput(
            attrs={
                'max_length': 100,
                'placeholder': 'Full Name'
            }
        )
    )
    idcard = forms.CharField(
        label='ID No.',
        widget=forms.TextInput(
            attrs={
                'max_length': 50,
                'placeholder': 'ID No.'
            }
        )
    )
    license_valid_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type':'date',
                'min': datetime.now().date(),
            }
        )
    )
    carrier = forms.ModelChoiceField(
        queryset=Carrier.objects.none(),
        widget=forms.Select(
            attrs={
                'placeholder': 'Select Carrier'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        # self.user = getattr(self, 'user', None)
        if not (self.user.is_superuser and self.user.is_staff):
            self.fields['carrier'].queryset = Carrier.objects.filter(users__username=self.user.username)
        else:
            self.fields['carrier'].queryset = Carrier.objects.all()
            
        self.helper = FormHelper(self)
        self.helper.form_tag = False
    
    class Meta:
        model = Driver
        fields = ('fullname', 'idcard', 'license_valid_date', 'active', 'carrier')