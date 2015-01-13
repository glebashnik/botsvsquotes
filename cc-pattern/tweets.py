# coding: utf-8

# Twitter search + mining example.

# This scripts doesn't "do" anything creative.
# It demonstrates how you can populate a .csv file with mined tweets.
# It is very useful as a template
# (i.e., you can copy and adapt it to create various Twitter crawlers,
#  then import the data from local .csv files into other projects).

from pattern.web import Twitter

# The pattern.db module has tools to work with data:
# SQLite and MySQL databases, .csv files, date parsers, ...
# The easiest way to store structured data is as a CSV
# ("comma-separated values"), a plain text file where
# each new line is a new row of data, and where columns
# are separated by ",".
# http://www.clips.ua.ac.be/pages/pattern-db#datasheet
from pattern.db import Datasheet
from pattern.db import pd

# The pd() function means: 
# "there is a file search2-data.csv" in the same folder as this script".
PATH = pd("tweets.csv")
#print PATH

try:
    # If a .csv file already exists, open that one and append new data to it.
    csv = Datasheet.load(PATH)
    seen = set(csv.columns[0])
except:
    # If a .csv file doesn't exist yet, create a new one.
    csv = Datasheet()
    seen = set()
    
# The "seen" variable is a set (= list of unique values)
# that contains the values in the first column in the CSV.
# In other words, it contains the id's of the tweets.
# We can use it to check if we have already seen a tweet,
# so we don't store it twice.

# Search for tweets containing the given search query:
q = "charlie hebdo"

twitter = Twitter(language="en", license=None)

id = None
for i in range(3):
    # Look for tweets containing the search query.
    # We can get a maximum of 100 tweets per search.
    # Don't cache the results locally, 
    # so we get the latest new tweets when the script runs.
    # Do this 3x.
    for tweet in twitter.search(q, start=id, count=100, cached=False):
        id = tweet.id
        if id not in seen:
            print tweet.text
            print
            seen.add(id)
            csv.append([
                tweet.id,
                q,
                tweet.author,
                tweet.text,
                tweet.retweets,
                tweet.date
            ])
    # Update the CSV.
    csv.save(PATH)
    
# Each time you run the script, new tweets will be appended to the CSV.
# For example, we have Twitter miners that automatically run 10x each day,
# and have been running for many days and weeks.

# We can then import the data in other scripts, e.g.:

#from pattern.db import Datasheet, pd
#csv = Datasheet.load(pd("tweets.csv"))
#for id, q, author, text, retweets, date in csv:
#    print text