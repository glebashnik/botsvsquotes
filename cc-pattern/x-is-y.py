# coding: utf-8

# Twitter search example.

from pattern.web import Twitter
from pattern.en import parsetree
from pattern.search import search

import re

who = "Justin Bieber"

twitter = Twitter()

# Look for tweets that mention "Justin Bieber is X".
# With count=100, Twitter.search() returns up to a 100 tweets.
# With start=i, and i=1->4, we call it 4x to get a total of 400 tweets.
# With cached=True, results are cached on the hard drive
# (if we run the query again it won't go online but use the local results).
# http://www.clips.ua.ac.be/pages/pattern-web#services
# http://www.clips.ua.ac.be/pages/pattern-web#twitter

# Twitter gives us about 350 queries per hour (or about 1 per 10 seconds).
# If you exceed that, Twitter.search() will raise an error.
# Right, now, you are sharing a default license key with all other Pattern users,
# so the 350 query limit will deplety rapidly.
# You can also get your own license key:
# https://apps.twitter.com/app/new

# And then use that key:
#LICENSE = ("OAuth goes here", "OAuth key goes here", ("OAuth secret", "OAuth token"))
#twitter = Twitter(license=LICENSE)

for i in range(1, 4):
    for tweet in twitter.search("\"%s is\"" % who, start=i, count=100, cached=True):
        
        s = tweet.text
        s = s.lower()
        s = re.sub(r"http://.*?(\s|$)", "", s) # Remove URL's.
        s = parsetree(s, lemmata=True)

        for m in search(who.lower() + " be {JJ}", s):
            # Find properties: "Justin Bieber is heartless".
            # This search pattern looks for the verb "to be" followed by an adjective.
            # Since we use parsetree(lemmata=True) conjugations like "am", "is", "was"
            # are also valid.
            # http://www.clips.ua.ac.be/pages/pattern-en#parser
            # http://www.clips.ua.ac.be/pages/pattern-search
            print m.group(1).string
        
        for m in search(who.lower() + " be {NP}", s):
            # Find categories (1): "Justin Bieber is a real nigga".
            # This search pattern looks for the verb "to be" followed by a noun phrase.
            # The parsetree() function identifies words that belong together.
            # For example, determiners (a, an), adjectives and nouns make up
            # noun phrases (NP's): "the black cat" is one entity.
            # Another example are verb phrases (VP's): "might be raining".
            print m.group(1).string
        
        for m in search(who.lower() + " be {NP PP NP}", s):
            # Find categories (2): "Justin Bieber is the global equivalent of ass cancer".
            # This search pattern looks for "to be" followed by a noun phrase,
            # followed by a preposition (in, on, of, with) followed by a noun phrase.
            # This catches more elaborate expressions than (1).
            print m.group(1).string
            
        for m in search(who.lower() + " be {VBG PP NP}", s):
            # Find actions: "Justin Bieber is pining for ex Selena Gomez".
            # This search pattern looks for -ing verbs followed by a prepositional noun phrase.
            # Verbs in the present participle tense are tagged as VBG: "eating", "sleeping", ...
            print m.group(1).string

# Note: parsing part-of-speech tags, lemmata and phrases uses a statistical approach.
# The English parser is quite good; it has a statistical accuracy of 95%.
# However, this also means that each 1/20 words is tagged wrong.
# So be prepared for the occasional weird result.
# One way to deal with this is to remove outliers.
# For example, you can keep a count of each result,
# and filter out those results that only occur once (e.g., "Justin Bieber is such"), 
# or assign more weight to results that occur often (e.g., "Justin Bieber is gay").

# What can we do with it?
# We can use this knowledge to automatically populate a semantic network, for example.
# We can run the script for a list of celebrities, and start mixing the results:

# - Justin Bieber is awesome
# - Justin Bieber is the global equivalent of ass cancer
# - George Clooney is hot
# - George Clooney is the next president
# - Goldilocks is a weirdo
# - Goldilocks is waiting for us
# - Hillary Clinton is a clown
# - Hillary Clinton is the next president
# - Hillary Clinton is signing books
# - Chewbacca is naked
# - Chewbacca is kind
# - Chewbacca is loving
# - Jesus is kind
# - Jesus is loving
# - Jesus is the foundation for racial harmony

# So, by inference, does this mean that "the next president is a clown"?
# Or that "ass cancer is awesome"?
# Or that "Chewbacca is the foundation for racial harmony"?