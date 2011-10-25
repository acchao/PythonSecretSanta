"""
Forms and validation code for user registration.
"""
import re

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from registration.models import RegistrationProfile

alnum_re = re.compile(r'^\w+$')
attrs_dict = { 'class': 'required' }

class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and requires 
        the password to be entered twice to catch typos.
    """
    username = forms.CharField(max_length=30, 
                               widget=forms.TextInput(attrs=attrs_dict), 
                               label=_(u'Username'))
    email = forms.EmailField(maxlength=75, 
                             widget=forms.TextInput(attrs=dict(attrs_dict)), 
                             label=_(u'Email address'))
    password1 = forms.CharField(label=_(u'Password')
                                widget=forms.PasswordInput(attrs=attrs_dict, 
                                                           render_value=False))
    password2 = forms.CharField(label=_(u'Confirm password'), 
                                widget=forms.PasswordInput(attrs=attrs_dict, 
                                                           render_value=False))
    
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already in use.
        """
        if not alnum_re.search(self.cleaned_data['username']):
            raise forms.ValidationError(_(u'Usernames can only contain letters, \
                                            numbers and underscores'))
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(u'This username is already taken.'))

    def clean_email(self):
        """
        Validate that the supplied email address is unique
        """
        try:
            user = User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_(u'This email address is already in use.'))
                                                                            
    def clean(self):
        """
        Verify that the values entered into the two password fields match.
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'Your passwords must match.'))
        return self.cleaned_data
    
    def save(self):
        """
        Create the new 'User' and 'RegistrationProfile', and returns the 'User'.
        """
        new_user = RegistrationProfile.objects.create_inactive_user(
                            username=self.cleaned_data['username'], 
                            password=self.cleaned_data['password1'], 
                            email=self.cleaned_data['email'])
        return new_user

