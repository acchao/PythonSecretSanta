from django.contrib import admin

from secretsanta.profiles.models import ParticipantProfile, RecipientMap

class ParticipantProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname',)

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.social_proof_verified: assignrecipient.main()

class RecipientMapAdmin(admin.ModelAdmin):
    list_filter = ('gift_shipped','gift_received')
    list_display = ('participant_id','recipient_id','gift_shipped','gift_received')

admin.site.register(ParticipantProfile, ParticipantProfileAdmin)
admin.site.register(RecipientMap, RecipientMapAdmin)

