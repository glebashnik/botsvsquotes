# coding: utf-8

# Natural language processing example.

from pattern.en import lexicon
from pattern.en import parsetree
from pattern.en import sentiment
from pattern.vector import shuffled

# We want to play with the "polarity" of adjectives.
# For example, "good" has a positive polarity and "bad" has a negative polarity.
# If we have a text that contains the word "good", can we make it more dramatic,
# by replacing "good" with an adjective that has an even more positive polarity?

# First, we'll construct a dictionary of {adjective: polarity score}.
# We can use Pattern's English lexicon to look for adjectives.
# Adjectives in the lexicon will be tagged with "JJ".
# Here is an overview of all possible tags:
# http://www.clips.ua.ac.be/pages/penn-treebank-tagset

# To find the polarity score of an adjective,
# we can use Pattern's sentiment function.
# It returns a (polarity, subjectivity)-tuple,
# two values that range between 0.0 and 1.0.
# For example: sentiment("good") => (0.7, 0.6)
# http://www.clips.ua.ac.be/pages/pattern-en#sentiment

adjectives = {}
for word, tag in lexicon.items():
    if tag == "JJ":
        adjectives[word] = sentiment(word)[0]

def dramatize(s):
    
    """ Returns a string with stronger adjectives:
        dramatize("This code is nice") => "This code is legendary"
    """
    
    x = []
    
    # A parse tree takes a string and returns a list of sentences,
    # where each sentence is a list of words, where each word is an
    # object with interesting attributes such as Word.tag.
    for sentence in parsetree(s):
        for word in sentence:
            replaced = False
            if word.tag == "JJ":
                
                # What's the polarity of this adjective?
                polarity = sentiment(word.string)[0]
                
                # Don't change neutral adjectives like "last", "political", ...
                if polarity != 0.0:

                    # Can we find an adjective in our dictionary
                    # with a more extreme polarity?
                    # Note: the shuffled() function takes a list 
                    # and returns a new, randomly ordered list. 
                    for w, p in shuffled(adjectives.items()):
                        if polarity >= 0 and p > polarity + 0.2 \
                        or polarity <  0 and p < polarity - 0.2:
                            x.append(w.lower())
                            replaced = True
                            break
            if not replaced:
                x.append(word.string)
                
    return " ".join(x)

opinion = "It's satisfying how well this cheap vacuum cleaner works. " + \
          "The suction power is amazing. Best part is the clear canister - " + \
          "you can see with your own eyes all the dirt coming out of your floor. " + \
          "We have 2 cats, and the amount of cat hair it pulled out of our carpet is scary!"

print dramatize(opinion)

# The scripts needs more fine-tuning obviously, 
# but look at the eloquence of this dramatized review:

# "It's magnificent how well this gorgeous vacuum cleaner works. 
#  The suction power is excellent. Best part is the sprightly canister - 
#  you can see with your exquisite eyes all the dirt coming out of your floor. 
#  We have 2 cats, and the amount of cat hair it pulled out of our carpet is devastating!"
