from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

from secretsanta.profiles.models import ParticipantProfile
from secretsanta.profiles.forms import ParticipantProfileForm


@login_required
def profile(request):
    """
    View the profile if it exists; return the create template if it doesn't.
    If there is a username in the request that doesn't match the logged in user, 
        return an error message.
    """
    template_name = 'profile.html'

    try:
        profile = request.user.get_profile()
        form = None
    except ObjectDoesNotExist:
        profile = None
        if request.method == 'POST':
            update_user = User.objects.get(username='%s' %request.user.username)
            if profile:
                form = ParticipantProfileForm(request.POST, instance=profile)
                if form.is_valid():
                    profile = form.save(commit=False)
                    profile.save()
                    return HttpResponseRedirect('/')
            else:
                form = ParticipantProfileForm(request.POST)
                if form.is_valid():
                    profile = form.save(commit=False)
                    profile.user_id = request.user.id
                    profile.save()
                    return HttpResponseRedirect('/')
        else:
            form = ParticipantProfileForm(instance=profile)
            form.email = request.user.email

    data = { 'profile': profile, 'form': form, }

    return render_to_response(template_name, 
                              data, 
                              context_instance=RequestContext(request))


@login_required
def edit(request,username):
    template_name = 'profile-edit.html'

    permission = has_permission(request.user, request.user.username, username)
    error_message = None
    if permission is not True:
        error_message = 'You do not have permission to edit this profile.'

    try:
        profile = request.user.get_profile()
    except ObjectDoesNotExist:
        profile = None

    profile = request.user.get_profile()

    if request.method == "POST":
        form = ParticipantProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = ParticipantProfileForm(instance=profile)

    data = { 'profile': profile, 'form': form, 'username': username }

    return render_to_response(template_name, 
                              data, 
                              context_instance=RequestContext(request))


def has_permission(request_user, request_username, username):
    """
    User must be logged in to proceed.
    Username in the request must match the logged in user.
    Only using this on edit - requesting to view another user's profile
        returns an error anyway.
    """
    if not request_user.is_authenticated():
        return False
    if cmp(request_username, username) != 0:
        return False
    return True


