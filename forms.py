#! /etc/bin/python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext as _


class LogInForm(forms.Form):
    """
    Default login form, uses username and password for standard authentication in django.contrib.auth
    """
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=100)


class UserForm(ModelForm):
    """
    Form wrapper for User in django.contril.auth
    """
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

    class Meta:

        model = User
        fields = ['email', 'username', 'password']
        labels = {
            'email': _('Email'),
            'username': _('Username'),
            'password': _('Password'),
        }
        error_messages = {
            'username': {
                'required': _('Username field is required'),
                'invalid': _('Username field is invalid')
            },
            'password': {
                'required': _('Password field is required'),
                'invalid': _('Password field is invalid')
            }, }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'validate', 'required': 'required'}),
            'last_name': forms.TextInput(attrs={'class': 'validate', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'validate', 'required': 'required'}),
            'username': forms.TextInput(attrs={'class': 'validate', 'required': 'required'}),
            'password': forms.TextInput(attrs={'class': 'validate', 'required': 'required'}),
        }

    def clean_email(self):
        """
        Verification for unique email
        :return: Email or raise exception
        """
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('duplicate email')

    def save(self, commit=True):
        """
        Custom save method for determine active and unactive users
        :param commit:
        :return:
        """
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False
            user.save()
        return user