from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views

from secretsanta.profiles import views

urlpatterns = patterns('',
    url(r'^edit/(?P<username>\w+)/$',   views.edit,             name='profiles_edit'),
    url(r'^$',                          views.profile,          name='profiles_profile'),
)

