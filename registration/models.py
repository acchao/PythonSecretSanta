import datetime
import random
import re
import sha

from django.conf import settings
from django.db import models
from django.http import Http404
from django import forms
from django.forms import ModelForm
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

SHA1_RE = re.compile('^[a-f0-9]{40}$')

class RegistrationManager(models.Manager):
    """
    Custom manager for the 'RegistrationProfile' model.
    """
    def activate_user(self, activation_key):
        """
        Validate an activation key and activate the corresponding 'User' if valid.
        - If the key is valid and has not expired, return the 'User' after activating.
        - If the key is not valid or has expired, return 'False'.
        - If the key is valid but the 'User' is already active, return 'False'.
        To prevent reactivation of an account which has been deactivated by site administrators, the key is reset to 'ALREADY_ACTIVATED' after successful activation.
        """
        # Make sure the key we're trying conforms to the pattern of a SHA1 hash; if it doesn't, no point trying to look it up in the database.
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                user = profile.user
                user.is_active = True
                user.save()
                profile.activation_key = "ALREADY_ACTIVATED"
                profile.save()
                return user
        return False
    
    def create_inactive_user(self, username, password, email, send_email=True):
        """
        Create a new, inactive 'User', generate a 'RegistrationProfile' and email its activation key to the 'User', returning the new 'User'.
        
        To disable the email, call with 'send_email=False'.
        """
        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()
        
        registration_profile = self.create_profile(new_user)
        
        if send_email:
            from django.core.mail import send_mail
            current_site = Site.objects.get_current()
            subject = render_to_string('activation_email_subject.txt', { 'site': current_site }) # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            message = render_to_string('activation_email.txt', { 'activation_key': registration_profile.activation_key, 'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS, 'site': current_site })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [new_user.email])
        return new_user

    def create_profile(self, user):
        """
        Create a 'RegistrationProfile' for a given 'User', and return the 'RegistrationProfile'.
        
        The activation key for the 'RegistrationProfile' will be a SHA1 hash, generated from a combination of the ``User``'s username and a random salt.
        """
        salt = sha.new(str(random.random())).hexdigest()[:5]
        activation_key = sha.new(salt+user.username).hexdigest()
        return self.create(user=user, activation_key=activation_key)
        
    def delete_expired_users(self):
        """
        Remove expired instances of 'RegistrationProfile' and their associated 'User's.
        
        Any 'User' who is both inactive and has an expired activation key will be deleted.
        
        To disable an account while keeping it in the database, just delete the RegistrationProfile.
        """
        for profile in self.all():
            if profile.activation_key_expired():
                user = profile.user
                if not user.is_active:
                    user.delete()

class RegistrationProfile(models.Model):
    """
    A simple profile which stores an activation key for use during user account registration.
    """
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    activation_key = models.CharField(_('activation key'), max_length=40)
    
    objects = RegistrationManager()
    
    class Meta:
        verbose_name = _('registration profile')
        verbose_name_plural = _('registration profiles')
    
    def __unicode__(self):
        return u"Registration information for %s" % self.user
    
    def activation_key_expired(self):
        """
        Determine whether this RegistrationProfile's activation key has expired, returning a boolean 'True' if the key has expired.
        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == "ALREADY_ACTIVATED" or (self.user.date_joined + expiration_date <= datetime.datetime.now())
    activation_key_expired.boolean = True

