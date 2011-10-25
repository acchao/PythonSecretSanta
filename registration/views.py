"""
Views which allow users to create and activate accounts.
"""
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound, Http404, HttpResponse, HttpResponseRedirect
from django import forms 
from django.shortcuts import render_to_response
from django.template import RequestContext

from secretsanta.registration.forms import RegistrationForm
from secretsanta.registration.models import RegistrationProfile
from secretsanta.profiles.models import ParticipantProfile

def activate(request, activation_key, template_name='activate.html'):
    """
    Activate a 'User' account, if their key is valid and hasn't expired.
    account: The 'User' object corresponding to the account, if the activation was successful. 'False' if the activation was not successful.
    expiration_days: The number of days for which activation keys stay valid after registration.

    If there are profile values in the session data, write those to the user profile when the account is created.
    """
    activation_key = activation_key.lower() # Normalize before trying anything with it.
    account = RegistrationProfile.objects.activate_user(activation_key)

    try:
        user = User.objects.get(username=account)
    except ObjectDoesNotExist:
        user = None

    if user:
        user_id = user.id
        session_data = dict(request.session.items())
        UserProfile.create_or_update(user_id, session_data)

    return render_to_response(template_name, {'account': account, 'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS }, context_instance=RequestContext(request))

def signup(request, success_url='/accounts/signup/complete/', form_class=RegistrationForm, profile_callback=None, template_name='signup_form.html'):
    """
    Allow a new user to register an account.

    TODO: If the user is already logged in, redirect to profile
    """
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save()
            n_username = new_user.username
            request.session['new_username'] = new_user.username
            request.session['new_email'] = new_user.email
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()

    return render_to_response(template_name, { 'form': form }, context_instance=RequestContext(request))

def get_initial_data(profile_obj):
    """
    Given a user profile object, returns a dictionary representing its fields, suitable for passing as the initial data of a form.
    """
    opts = profile_obj._meta
    data_dict = {}
    for f in opts.fields + opts.many_to_many:
        data_dict[f.name] = f.value_from_object(profile_obj)
    return data_dict


