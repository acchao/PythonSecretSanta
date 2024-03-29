# /Users/barbara/Code/tippit/openmedia/trunk/openmedia/userstuff/models.py

from django.conf import settings
from django.db import models
from django.http import Http404
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class ParticipantProfile(models.Model):
    """
    A basic profile which stores user information after the account 
        has been activated.
    Use this model as the value of the ``AUTH_PROFILE_MODULE`` setting
    """
    user = models.ForeignKey(User)
    first_name = models.CharField(max_length=40, blank=False)
    last_name = models.CharField(max_length=40, blank=False)
    address = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    state = models.CharField(max_length=2, blank=False)
    postal_code = models.CharField(max_length=6, blank=True, null=True)
    country = models.CharField(max_length=3, blank=False)
    # TODO: decide how to label this social_proof field in the forms
    social_proof = models.CharField(max_length=100, blank=False)
    social_proof_verified = models.BooleanField(default=False)
    likes = models.TextField("Likes/Wish Lists", blank=True)
    dislikes = models.TextField("Dislikes", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def fullname(self):
        return "%s, %s" %(self.last_name,self.first_name)
        fullname.short_description = 'Full Name'

    @staticmethod
    def create_or_update(user_id, data):
        """
        Pass in a user id and a data dict to update a user profile or create one
        """
        #clean up the data
        for k, v in data.copy().iteritems():
            if v == '':
                del data[k]
            else:
                try:
                    ParticipantProfile._meta.get_field(k)
                except:
                    del data[k]

        if data['first_name']: 
            data['first_name'] = str(data['first_name']).title()
        if data['last_name']: 
            data['last_name'] = str(data['last_name']).title()

        try:
            record = ParticipantProfile.objects.get(user=user_id)
            record.__dict__.update(data)
            record.save()
            return True
        except ParticipantProfile.DoesNotExist:
            data.update({'user_id': user_id})
            ParticipantProfile(**data).save()
            return True

    class Meta:
        ordering = ['last_name']


class RecipientMap(models.Model):
    """
    Maps gift senders to recipients
    When a user has registered and Python community participation 
        confirmed ('social_proof_verified'), a record is written
        to this table assigning a gift recipient to the participant.
    Includes optional 'sent' and 'received' dates
    """
    participant = models.ForeignKey(User, related_name='participant')
    recipient = models.ForeignKey(User, related_name='recipient')
    gift_shipped = models.DateField(null=True, blank=True)
    gift_received = models.DateField(null=True, blank=True)

    def relationship(self):
        return u"%s >> %s" % (self.participant, self.recipient)
        relationship.short_description = 'Rel'

    class Meta:
        ordering = ['gift_shipped']
        unique_together = ("participant", "recipient",)

