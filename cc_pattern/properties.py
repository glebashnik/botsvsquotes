# coding: utf-8

# This script is a mash-up of other scripts.

# You should have a look at the following scripts first:
# - celebrities.py (deals with Wikipedia mining),
# - dramatize.py   (deals with part-of-speech tagging),
# - tweets.py      (deals with Twitter mining + CSV databases)

# In summary, this script constructs a list of known celebrities
# (= people that have been on the cover of Rolling Stone),
# then it collects tweets that mention these people,
# then it extracts adjectives from those tweets,
# and finally creates a tuple store (person -> adjective) in a .csv file.

# We can think of this dataset as a collection of "properties"
# that popular vote has alloted to known celebrities.

# If you rerun this script, it will add new data to the dataset 
# (so far we have +50,000 tuples).

from pattern.web import Wikipedia
from pattern.web import plaintext

from pattern.web import Twitter
from pattern.db import Datasheet, pd

from pattern.en import parsetree

# ------------------------------------------------------------------------------------
# See celebrities.py

def celebrities():
    """ Returns a list of celebrities from Wikipedia.
    """
    celebrities = set()
    w = Wikipedia(language="en")
    p = w.search("List of people on the cover of Rolling Stone", cached=True)
    s = p.plaintext()
    for section in p.sections:
        if section.parent and section.parent.title in ("Individuals",):
            for name in section.links:
                if "* " + name in s:
                    celebrities.add(name)
    return celebrities

# ------------------------------------------------------------------------------------
# See dramatize.py

def adjectives(s):
    """ Returns a list of adjectives in the given string.
    """
    a = set() # set ~= list of unique values
    t = parsetree(s)
    for sentence in t:
        for word in sentence.words:
            if word.tag and word.tag == "JJ":
                a.add(word.string.lower())
    return list(sorted(a))

#print adjectives("I'm melting! Meeelting! What a wicked and cruel world!")
    
# ------------------------------------------------------------------------------------
# See tweets.py

csv = Datasheet()

PATH = pd("properties.csv")

try:
    csv = Datasheet.load(PATH)
    seen = set(csv.columns[0])
except:
    csv = Datasheet()
    seen = set()

twitter = Twitter(language="en", license=None)

for name in celebrities():
    id = None
    for tweet in twitter.search(name, start=id, count=100, cached=False):
        id = tweet.id
        if id not in seen:
            print name, tweet.text
            print
            seen.add(id)
            for w in adjectives(tweet.text):
                if not w.startswith(("@", "~", "1", "2")): # filter out weirdness
                    csv.append([tweet.id, name, w])
    csv.save(PATH)

# ------------------------------------------------------------------------------------
# Dataset reader.

PATH = pd("properties.csv")

f = {} # {celebrity: {property: count}}
for id, name, p in Datasheet.load(PATH):
    if name not in f:
        f[name] = {}     # {"Justin Bieber": {}}
    if p not in f[name]:
        f[name][p] = 0   # {"Justin Bieber": {"gay": 0}}
    f[name][p] += 1      # {"Justin Bieber": {"gay": 1}}
        
#print f["Eminem"]

for name in f:
    properties = f[name]                                 # {"problematic": 1}
    properties = [(v, k) for k, v in properties.items()] # [(1, "problematic"), ...]
    properties = sorted(properties, reverse=True)
    salient = properties[:3]
    print name, salient
    
# Jennifer Lopez -> old, sexy, bad
# Barack Obama   -> beautiful, significant, proud
# Andy Warhol    -> ~, plastic, pink
