# /Users/barbara/Code/tippit/openmedia/trunk/openmedia/userstuff/forms.py

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from secretsanta.profiles.models import ParticipantProfile
from secretsanta.profiles.data.countries import countries

class ParticipantProfileForm(ModelForm):
    country = forms.ChoiceField(label='Country', widget=forms.Select(attrs={'class':'input_select'}), choices=countries, required=False)

    def clean_first_name(self):
        if 'first_name' in self.cleaned_data: self.cleaned_data['first_name'] = str(self.cleaned_data['first_name']).title()
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        if 'last_name' in self.cleaned_data: self.cleaned_data['last_name'] = str(self.cleaned_data['last_name']).title()
        return self.cleaned_data['last_name']

    class Meta:
        model = ParticipantProfile
        exclude = ('user',)


