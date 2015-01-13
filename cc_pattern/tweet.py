# coding: utf8

# This script can be used to post new tweets on Twitter.

# You'll need a version of Pattern from GitHub 
# *more recent than* Jan 8, 2015:
# https://github.com/clips/pattern/archive/master.zip

# Pattern has tools to collect data from Google, Twitter, Wikipedia, ...
# But there are no tools to post new tweets, edit Wikipedia articles, ...
# There's a good reason. Pattern is for learning data mining, not for spamming and trolling.

# So if we want to create a Twitter bot that posts tweets, 
# we need to write the post code ourself.

# Nevertheless, we can reuse Pattern's source code to make life easier
# (authentication on the Twitter API is a hassle).

# Here is a test account: @ccpattern
# We've set up the account with a license key 
# that allows posting new tweets
# (which is disabled by default):
ccpattern = (
    "oMRJ43mxBd9gmmibzuvXTmbUS",
    "8zGpmlg7bprmvoTMEGnny8De13ccFI8A3d7VjmQNaoFphXm67V", (
    "2969891194-RgOh55fKo1AzdepC4hALyQ4oQDg0xnGf2IHR0Ev",
    "pw5bJxV7A5PkDnTH3QDCYgkHmB1IBwybo4FE1OWJFTQlT")
)

# @ccpattern is followed by Selena Gomez!
# We better post some good stuff so she notices us.
# Tip: we could create a bot that follows everyone,
# hope they follow us back, and then invent tweets that address them.

from pattern.web import URL, Twitter

# Tweet to post:
tweet = "avalancheddar"

# The API for posting is described here:
# # https://dev.twitter.com/rest/reference/post/statuses/update
url = URL("https://api.twitter.com/1.1/statuses/update.json", method="post", query={"status": tweet})

# We'll use the Twitter._authenticate() method to authenticate ourselves 
# as @ccpattern (so the new tweet will appear on @ccpattern's page):
twitter = Twitter(license=ccpattern)
url = twitter._authenticate(url)

try:
    # Send the post request.
    url.open()
except Exception as e:
    print e
    print e.src
    print e.src.read()
    
# To create your own Twitter bot:

# 1) You need a new e-mail address for the bot (e.g., gmail.com).
# 2) You need a new Twitter account.
# 3) Verify the Twitter account from the e-mail they send you.
# 4) Verify the Twitter account with a mobile phone number (this is mandatory): 
#   https://support.twitter.com/articles/110250-adding-your-phone-number-to-your-account
# 5) While logged in in the new account, create a Twitter App:
#   https://apps.twitter.com/app/new
# 6) Modify the app's permissions to "read & write".
# 7) Regenerate the keys and access tokens.
# 8) Paste the keys and access tokens into this script instead of @ccpattern's keys.
