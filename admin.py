from django.contrib import admin
from django.contrib.auth.models import User, Group

class AdminSite(admin.AdminSite):
    pass

site = AdminSite()

site.register(User)
site.register(Group)
