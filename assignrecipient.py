import sys
import sqlite3 as sqlite

from django.template.loader import render_to_string

import secretsanta.settings as settings

def assign(participantid):
    """
    Pass in the ParticipantProfile object,  
    identify an eligible gift recipient and 
    create the gifter-giftee record (recipientmap)
    """
    conn = sqlite.connect(settings.DATABASES['default']['NAME'])
    curs = conn.cursor()

    # Get a verified User who has not already been assigned as a gift recipient yet 
    # and whose user_id is not the same as participantid
    t = (participantid,)
    curs.execute("SELECT user_id FROM profiles_participantprofile WHERE \
                 user_id NOT IN (SELECT recipient_id FROM profiles_recipientmap) \
                 AND social_proof_verified = 'true' AND user_id != ? LIMIT 1", t)
    print curs.fetchall()

    # TODO: What to do if there is not a free recipient?  
    # seed data pre-launch?

    # insert to profiles_recipientmap: recipient_id = , participant_id = participantid
    # select the profile data where user_id = recipient_id and return that as 'giftmap'

    # conn.commit()
    curs.close()

    sys.exit()
    return giftmap 

def notify(gifteeprofile,gifteremail):
    """
    Send a notification email to the gifter (and giftee?)
    """
    fromaddr = "Python Secret Santa <admin@pythonsecretsanta.com>"
    toaddrs = gifteremail
    site = 'Python Secret Santa'

    message = render_to_string('gift_email.txt', {'site': site })
    msg = MIMEText(message)
    msg['Subject'] = "Your Python Secret Santa gift recipient"
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddrs)

    server = smtplib.SMTP('localhost')
    # server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def main(obj):
    """
    Triggered by setting social_proof_verified to 'true' in the admin.

    TODO: write the methods to:
        1) create the gifter-giftee record (recipientmap)
        2) send a notification email to the gifter (and giftee?)
    """
    # print obj.id
    giftmap = assign(obj.user_id)
    notify(giftmap, obj.email)
    
if __name__ == "__main__":
    main()

