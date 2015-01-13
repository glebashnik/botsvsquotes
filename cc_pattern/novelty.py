# coding: utf-8

# Bing search example.

from pattern.web import Bing

# Part of the challenge of computational creativity is evaluation: 
# programs that figure out how novel their find is.
# This script offers a naive approach that many people will also use: "Google it".

def novelty(word):
    
    """ Returns the novelty of the given word as a value 0.0-1.0 (1.0 = 100% novel).
    """
    
    engine = Bing() # Google(license="...")
    
    # Get the number of search results that mention the given word.
    # http://www.clips.ua.ac.be/pages/pattern-web#services
    count = engine.search(word, cached=True).total
    
    # Note: we should cached=False to get the most up-to-date count.
    
    # It would be nice if this number was relative (0.0-1.0),
    # then we could represent novelty as a percentage,
    # based on the number of existing web pages that mention the word.
    # Here are some raw numbers:
    
    # - "and"                      : 1730000000
    # - "new york"                 : 94700000
    # - "tree"                     : 78200000
    # - "justin bieber"            : 7680000
    # - "computational creativity" : 5330000
    # - "zombification"            : 126000
    # - "zombification machine"    : 37000
    # - "zombology"                : 11100
    # - "zombeliever"              : 11
    # - "zombriefing"              : 0
    # - "zombifractor"             : 0
    
    # So, it looks like common words are mentioned thousands of times,
    # while invented words are mentioned dozens of times.
    
    # We'll cut off the result count above 100
    # (= anything mentioned 100x times on the net is not novel).
    count = min(count, 100)
    
    # And then relativize the value:
    count = 1.0 - count * 0.01
    
    return count

print novelty("zombie")      # 0.0, nothing new
print novelty("zombeliever") # 0.9, quite novel
print novelty("zombriefing") # 1.0, new word!
print

# Note: 
# Bing gives us about 5,000 free queries per month.
# Google gives us about 100 free queries per day.
# If you need more, you need to obtain a license key:
# http://www.clips.ua.ac.be/pages/pattern-web#license
# Services like Bing and Google require you to enter a credit card number.
# They will charge you, but the rates are not so high (e.g., 1$ for 500 Bing queries).

# ------------------------------------------------------------------------------------

# The word "zombriefing" is quite interesting, for two reasons we can think of.
# 1) Suffix "-bie" and prefix "brie-" are almost identical and go together nicely.
# 2) Semantically, "briefing" refers to a one-sided kind of meeting,
#    where a meeting is a form of communication that many people find mindless;
#    whereas "zombies" are mindless and can't communicate.
#    There is a vaguely humoristic connection between the two concepts.
#    How about: "the drill sergeant zombriefed the men" ?

# To simulate (2) algorithmically, we'd need lots of learning material.
# Let's see if we can simulate (1) with a few tricks.

from pattern.metrics import similarity

# The similarity() function computes (1 - the Levenshtein distance):
# http://www.clips.ua.ac.be/pages/pattern-metrics#similarity
# The higher the number (0.0-1.0), the more similar two strings are.
print similarity("bie", "brie") # 0.75

# So, given a word (e.g., "briefing"), we could look for a second word 
# that we can glue to the left of it - if the prefix of the given word 
# and the suffix of the second word are sufficiently similar
# (e.g., similarity >= 0.75) ...

from pattern.en import lexicon # English {word: word type}-dictionary

w1 = "briefing"

for w2 in lexicon.keys():
    if w2[0].isupper(): # Exclude proper names like "Herbie".
        continue
    if len(w2) <= 3:    # Length of "zombie" > 3, OK.
        continue
    if w2[-3] != w1[0]: # zom[b]ie == [b]riefing, OK.
        continue
    if similarity(w2[-3:], w1[:4]) >= 0.75: # similarity("bie", "brie") >= 0.75, OK.
        print w2, "=>", w2[:-3] + w1,
        if w2[-3:] != w1[:3]:
            # These cases are somewhat special: 
            # "professor" <=> "snoring"
            print "(!)"
        else:
            # These cases are less creative:
            # "elegant" <=> "anteater"
            print 
            
# This still needs a lot of work (or an entirely different approach).
# Some (hand-picked) results are funny though. 
# How about: 
# - "professnoring"
# - "sacrificheddar"
# - "breakfastronaut"
# - "garden shrugby"
# - "calendwarf", 
# - ".50-calibeer"
# - "comediscourse"
# - "step-by-steapot"
# - "laundromath"
# - "grandchildreindeers"
