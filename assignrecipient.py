import sys, smtplib
from email.mime.text import MIMEText

from django.contrib.auth.models import User
from django.template.loader import render_to_string

import secretsanta.settings as settings
from secretsanta.profiles.models import ParticipantProfile, RecipientMap

def assign(participant):
    """
    - Pass in the ParticipantProfile object
    - Identify an eligible gift recipient
    - Create the gifter-giftee record (recipientmap)
    - Return the giftee record so mailing information can be sent to the gifter
    """
    giftmap = []

    try:
        # Get a verified User who has not already been assigned as a gift recipient yet 
        # and whose user_id is not the same as participantid
        rec = ParticipantProfile.objects.filter(social_proof_verified=True) \
                    .exclude(user=participant.user) \
                    .extra(select={'exclusion': 'SELECT recipient_id FROM profiles_recipientmap'},)[:1]
        recipient = rec[0]
    except ParticipantProfile.DoesNotExist:
        # TODO: What to do in case there is not a free recipient?
        print "No available gift recipient"
        sys.exit()

    # Add'l check to ensure participant is not assigned to more than one recipient
    try:
        r = RecipientMap.objects.get(participant=participant.id)
    except RecipientMap.DoesNotExist:
        # Create the recipientmap record, assigning the participant to a gift recipient
        m = RecipientMap(participant_id=participant.pk, recipient_id=recipient.pk)
        m.save()

    # Select the profile data where user_id = recipient_id and return as 'giftmap'
    # Include gift sender User object for email info
    ge = ParticipantProfile.objects.get(user=recipient.user)
    gr = User.objects.get(pk=participant.user_id)
    giftmap.append(ge)
    giftmap.append(gr)
    return giftmap

def notify(giftmap):
    """
    Send a notification email to the gifter (and giftee?)
    """
    giftee = giftmap[0]
    gifter = giftmap[1]

    fromaddr = "Python Secret Santa <admin@pythonsecretsanta.com>"
    toaddrs = gifter.email
    site = 'Python Secret Santa'

    message = render_to_string('gift_email.txt', {'site': site, 'address': giftee.address })
    msg = MIMEText(message)
    msg['Subject'] = "Your Python Secret Santa gift recipient"
    msg['From'] = fromaddr
    msg['To'] = toaddrs

    server = smtplib.SMTP('localhost')
    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, str(msg))
    server.quit()

def main(obj):
    """
    Triggered by setting social_proof_verified to 'true' in the admin.
    """
    giftmap = assign(obj)
    notify(giftmap)
    
if __name__ == "__main__":
    main()

