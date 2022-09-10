from dataclasses import field
from operator import attrgetter
from statistics import mode
from tkinter import SE, Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer
from app.models import Customer



class CustomerRegistrarionForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'stext-111 cl2 plh3 size-116 p-l-10 p-r-30'}))
    password2 = forms.CharField(label='Confirm Password (again)',widget=forms.PasswordInput(attrs={'class':'stext-111 cl2 plh3 size-116 p-l-10 p-r-30'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'stext-111 cl2 plh3 size-116 p-l-10 p-r-30'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email':'Email'}
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'stext-111 cl2 plh3 size-116 p-l-10 p-r-30'}))
    password = forms.CharField(label=_('password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'stext-111 cl2 plh3 size-116 p-l-10 p-r-30'}))


class MyPasswordChangeForm(PasswordChangeForm):
        old_password = forms.CharField(label=('Old Password'),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus':True, 'class':'form-control'}))
        new_password1 = forms.CharField(label=('New Passwoed'),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
        new_password2 = forms.CharField(label=('Confirm New Passwoed'),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))



class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=('E-mail'), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))



class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=('New Passwoed'),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=('Confirm New Passwoed'),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))






class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','state','zipcode']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
        'locality':forms.TextInput(attrs={'class':'form-control'}),
        'city':forms.TextInput(attrs={'class':'form-control'}),
        'state':forms.TextInput(attrs={'class':'form-control'}),
        'zipcode':forms.NumberInput(attrs={'class':'form-control'})
        }