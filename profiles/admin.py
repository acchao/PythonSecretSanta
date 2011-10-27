from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

from secretsanta.profiles.models import ParticipantProfile, RecipientMap
from secretsanta.profiles.data.countries import countries
from secretsanta import assignrecipient

class CustomParticipantProfileForm(forms.ModelForm):
    country = forms.ChoiceField(label='Country', widget=forms.Select(
                attrs={'class':'input_select'}),
                choices=countries,
                required=False,
                )

    class Meta:
        model = ParticipantProfile

class ParticipantProfileAdmin(admin.ModelAdmin):
    list_display = ('fullname','id','social_proof_verified',)
    # readonly_fields=('user',)
    form = CustomParticipantProfileForm

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.social_proof_verified:
            assignrecipient.main(obj)

class RecipientMapAdmin(admin.ModelAdmin):
    list_filter = ('gift_shipped','gift_received')
    list_display = ('participant','recipient','gift_shipped','gift_received')

admin.site.register(ParticipantProfile, ParticipantProfileAdmin)
admin.site.register(RecipientMap, RecipientMapAdmin)

