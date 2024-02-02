from django import forms
from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper

from ..models import Vehicle, Carrier

from datetime import datetime
    
class VehicleForm(forms.ModelForm):
    valid_until = forms.DateField(
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
        if not (self.user.is_superuser and self.user.is_staff):
            self.fields['carrier'].queryset = Carrier.objects.filter(users__username=self.user.username)
        else:
            self.fields['carrier'].queryset = Carrier.objects.all()
            
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['registration_plate'].disabled = True
            self.fields['carrier'].disabled = True
    
    class Meta:
        model = Vehicle
        fields = ('registration_plate', 'vehicle_type', 'valid_until', 
                  'max_weight', 'max_cbm','active', 'carrier')