from django import forms
from .models import User
import re

class AddUserForm(forms.Form):
    name = forms.CharField(
        max_length=100, 
        required=True,
        error_messages={
            'required': 'field is required',
            'max_length': 'must not exceed 100 characters'
        }
    )
    email = forms.EmailField(
        max_length=100, 
        required=True,
        error_messages={
            'required': 'field is required',
            'invalid': 'must be a valid email address',
            'max_length': 'must not exceed 100 characters'
        }
    )
    password = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.PasswordInput,
        error_messages={
            'required': 'field is required',
            'max_length': 'must not exceed 100 characters'
        }
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('is already registered')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if len(password) < 8:
            raise forms.ValidationError('must be at least 8 characters long')
            
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('must contain at least one uppercase letter')
            
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError('must contain at least one lowercase letter')
            
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError('must contain at least one special character')
            
        return password