"""
URLConf for Django user registration and authentication.
"""

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views

from secretsanta.registration import views

urlpatterns = patterns('',
    url(r'^activate/(?P<activation_key>\w+)/$', views.activate, \
        name='registration_activate'),
    url(r'^$', views.signup, name='registration_signup'),
    url(r'^complete/$', direct_to_template, \
        {'template': 'registration_complete.html'}, 
        name='registration_complete'),
)
