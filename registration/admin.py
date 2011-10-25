from django.contrib import admin

from secretsanta.registration.models import RegistrationProfile

class RegistrationProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'activation_key_expired')
    search_fields = ('user__username', 'user__first_name')

admin.site.register(RegistrationProfile, RegistrationProfileAdmin)

