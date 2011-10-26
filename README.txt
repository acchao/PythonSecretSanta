Python Community Secret Santa

Rough Draft Thoughts:

1. Social signup - openid, facebook, twitter
2. Links in profiles to projects/sites/github/bitbucket repos 
    2a. proof of involvement - "social proof"
        (Isn't someone is going to have to hand-check all this "social proof"? We'll needs lots of little Santa's elves.)
3. 50$ USD or *under*
4. Donations to non profit organizations can be requested in lieu of gift
5. Links to wishlists in profiles (newegg, thinkgeek, amazon, etc)
6. Profiles should have "interests" and "dislikes" 
7. Important to note to factor in intl. shipping. Also, often, it's possible to order from a local store (like amazon.co.uk or a local shop) without incurring crazy shipping.
    7a. Might also want to match gifters/giftees by location (at least within the same country) to avoid int'l shipping.
8.  

Sites to link to:
- amazon
- maker store
- http://hackerthings.com/
- ???

profile fixtures: python manage.py loaddata profiles


TODO:

profiles/models.py - decide how to label this social_proof field in the forms

assignrecipient.py - write the methods to:
    1) create the gifter-giftee record (recipientmap)
    2) send a notification email to the gifter (and giftee?)

Proposed recipient assignment algorithm:
    When a user's 'proof of involvement' is marked as verified, he/she becomes eligible to receive a gift.
    The next user marked as verified will be assigned as a gifter to the most recent previous user who:
        - is also marked as verified
        - is not already a gift recipient (has not been assigned a gifter yet)
    Once a gifter has been matched with a giftee:
        - the gifter should receive an email with the recipient's contact info, likes/dislikes
        - the gifter's profile should also display the recipient's contact info, likes/dislikes
        - the giftee's profile should indicate that he/she has been matched with a gift sender, nothing else

get registration working (having a problem testing with local SMTP)

decide on dates:
    a. Deadline for signing up (after this date, gifter-to-giftee assignments are made among verified users)
    b. Deadline for shipping a gift (No way to enforce this of course, but recommending a date might encourage accountability - if a user does not mark his gift as shipped by this date, what happens? Anything?)
    c. Deadline for receiving a gift (Not so much a deadline as an expected date.  If a giftee has not received his gift by a certain date, is there any recourse against the gifter?)
    
Probably need some kind of privacy policy, or language to remind users that their personal contact information will be visible to another user.

