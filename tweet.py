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
    "clSJvo3yYHYuCz2CoJIss8YPd",
    "ErEVIZJbNnEAPMrV9RY4emczTKfuUsbgoTR41sTZuPHsL4Q22d", (
    "2976280017-0YW34DiaPFwGLjjoCmLp4550yHIbvouSGfmrkq3",
    "5ZnXSFeyHOFLjZ8dh7AzscYt88xOhZhBRMWxbOu86pE0z")
)

def post_tweet(tweet):
	from pattern.web import URL, Twitter
	import json

	url = URL("https://api.twitter.com/1.1/statuses/update.json", method="post", query={"status": tweet})

	twitter = Twitter(license=ccpattern)
	url = twitter._authenticate(url)

	try:
	    # Send the post request.
	    data = url.open().read()
	except Exception as e:
	    print e
	    print e.src
	    print e.src.read()
	    return None

	data = json.loads(data)
	return int(data[u'id'])

def reply_tweet(tweet, reply_id, reply_user="@BotsVsQuotes"):
	from pattern.web import URL, Twitter

	tweet = reply_user + " " + tweet
	url = URL("https://api.twitter.com/1.1/statuses/update.json", method="post", query={"status": tweet, "in_reply_to_status_id": reply_id})

	twitter = Twitter(license=ccpattern)
	url = twitter._authenticate(url)

	try:
	    # Send the post request.
	    url.open()
	except Exception as e:
	    print e
	    print e.src
	    print e.src.read()

def get_replies(reply_id):
	import json
	from pattern.web import URL, Twitter

	reply_id = reply_id - 1
	url = URL("https://api.twitter.com/1.1/statuses/mentions_timeline.json", method="get", query={"since_id":reply_id})

	twitter = Twitter(license=ccpattern)
	url = twitter._authenticate(url)

	user_replies = {}
	bot_replies = {}
	try:
	    data = json.loads(url.open().read())
	    for reply in data:
	    	name = reply["user"]["name"].encode('utf-8').strip()
	    	text = reply["text"].replace("@BotsVsQuotes","").strip()
	    	if name == "BotsVsQuotes":
	    		#bot quotes
	    		text = text.split(":") 
	    		char_name = text[0]
	    		bot_replies[char_name] = "".join(text[1:]).strip()
	    	else:
	    		#user quotes
	    		user_replies[name] = text 
	except Exception as e:
	    print e
	    print e.src
	    print e.src.read()
	    return {}, {}
	return bot_replies, user_replies



if __name__ == '__main__':
	import json
	from pattern.web import URL, Twitter

	# Tweet to post:
	tweet = "test tweet"

	url = URL("https://api.twitter.com/1.1/statuses/update.json", method="post", query={"status": tweet})

	twitter = Twitter(license=ccpattern)

	url = twitter._authenticate(url)


	try:
	    # Send the post request.
	    a = json.loads(url.open().read())
	    reply_id = a["id"]
	    print reply_id
	except Exception as e:
	    print e
	    print e.src
	    print e.src.read()





