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


Proposed models:

a) If we're using Django, all the standard stuff from the auth_user model:
username
firstname
lastname
email
password
etc.

b) Add'l bits in a profile model:
userid (pk, from auth_user)
street address
city
state / county
postal code
social proof
social proof verified (once verified, user is eligible for gifter/giftee assignment)
likes (I think this should just be a big text blob that can contain "likes", links to wishlists, requests for in lieu donations, etc.)
dislikes
date registered

c) Gifter-to-giftee:
gifter user id
giftee user id
gift shipped
gift received



I (Barbara) also want to propose that we establish some dates - all good swaps and gift exchanges have to have deadlines or they get out of hand pretty quickly:
    a. Deadline for signing up (after this date, gifter-to-giftee assignments are made among verified users)
    b. Deadline for shipping a gift (No way to enforce this of course, but recommending a date might encourage accountability - if a user does not mark his gift as shipped by this date, what happens? Anything?)
    c. Deadline for receiving a gift (Not so much a deadline as an expected date.  If a giftee has not received his gift by a certain date, is there any recourse against the gifter?)

I have managed a lot of gift exchanges and craft swaps and things like that in my time, and I have to point out that there are going to be some disappointments and headaches.  Some users will not come back and mark their gifts shipped or received. Sometimes people flake on shipping things - we can make it as easy as possible by providing links to Amazon, ThinkGeek, etc., but ultimately there will be a human element to deal with that just can't be automated or controlled.


