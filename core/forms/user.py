from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper

from ..models import Carrier, User
    
class UserForm(UserCreationForm):
    
    carrier = forms.ModelChoiceField(queryset=Carrier.objects.filter(active=True))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['username'].disabled = True
            
        self.helper = FormHelper(self)
        self.helper.form_tag = False
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'carrier', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'length': 150,
                'placeholder': 'Username',
                'hx-get': reverse_lazy('check_username'),
                'hx-trigger': 'keyup changed delay:1s',
                # 'hx-trigger': 'blur from:#id_username',
                'hx-target': '#div_id_username',
                'hx-swap': 'outerHTML',
            }),
            'first_name': forms.TextInput(attrs={
                'length': 150,
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'length': 150,
                'placeholder': 'Last Name'
            }),
        }
                
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    
    
class UserUpdateForm(forms.ModelForm):
    
    username = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['username'].disabled = True
            self.fields['carrier'].disabled = True
            
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'carrier', 'is_active')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'length': 150,
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'length': 150,
                'placeholder': 'Last Name'
            }),
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class SetUserPasswordForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(
        required=True,
        label='New password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'autofocus': True}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        instance = getattr(self, 'instance', None)
        self.username = instance.username
        if instance and instance.pk:
            self.fields['username'].disabled = True

        
    def clean_password(self):
        password = self.cleaned_data.get("password")
        password_validation.validate_password(password, User)
        return password

    def save(self, commit=True):
        password = self.cleaned_data["password"]
        user = User.objects.filter(username=self.username).first()
        user.set_password(password)
        if commit:
            user.save()
        return user
    
    class Meta:
        model = User
        fields = ('username', 'password')