# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import models as auth_models
from django.utils.translation import ugettext as _

from . import conf


class UserBaseForm(forms.ModelForm):
    """
    Form wrapper for User in django.contril.auth
    """
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = auth_models.User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
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
        print("Cleaning email {}".format(email))
        if conf.AUTH_UNIQUE_EMAIL:
            try:
                auth_models.User.objects.get(email=email)
            except UserBaseForm.DoesNotExist:
                return email
            raise forms.ValidationError('duplicate email')
        else:
            return email

    def save(self, commit=True):
        """
        Custom save method for determine active and unactive users
        :param commit:
        :return:
        """
        user = super(UserBaseForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            if conf.AUTH_VERIFY_EMAIL:
                user.is_active = False
            user.save()
        return user


class EmailPasswordForm(UserBaseForm):
    """
    Use just Email to login
    """

    class Meta(UserBaseForm.Meta):
        fields = (
            'email',
            'password'
        )

    def save(self, commit=True):
        """
        Custom save method for determine active and unactive users
        :param commit:
        :return:
        """
        user = super(UserBaseForm, self).save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            if conf.AUTH_VERIFY_EMAIL:
                user.is_active = False
            user.save()
        return user


class UsernameEmailPasswordForm(UserBaseForm):
    class Meta(UserBaseForm.Meta):
        fields = (
            'username',
            'email',
            'password'
        )
