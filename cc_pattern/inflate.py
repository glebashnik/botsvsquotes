# coding: utf-8

# Natural language processing example.

from random import choice

from pattern.en import parsetree, pluralize
from pattern.search import search

def inflate(s):
    
    """ Returns an exaggerated string:
        inflate("I'm eating a burger") => "I'm eating hundreds of burgers".
    """
    
    # Part-of-speech tagging identifies word types in a text.
    # For example, "can" can be a noun (NN) or a verb (VB),
    # depending on the words surrounding it.
    # http://www.clips.ua.ac.be/pages/pattern-en#parser
    
    # A parse tree splits punctuation marks from words, tags words,
    # and constructs a nested tree of sentences that contain words.
    # http://www.clips.ua.ac.be/pages/pattern-en#tree
    t = parsetree(s)
    
    # We can use pattern.search to search for patterns inside a parse tree.
    # If you know what regular expressions are: this is similar,
    # only you can also search by part-of-speech tag.
    # This is very useful to retrieve syntactic structures, e.g.:
    # "any noun, optionally preceded by an adjective", or
    # "any conjugation of the verb to be".
    # http://www.clips.ua.ac.be/pages/pattern-search
    
    # The search pattern below means:
    # "any determiner (a, an, the), optionally followed by any adjective,
    #  followed by one or more nouns".
    # The search will yield a list of matches.
    # We'll pluralize the nouns in each match, so that "burger" becomes "burgers", etc.
    # Note the curly braces {}.
    # We can retrieve the words inside it with match.group().
    for match in search("{DT} {JJ?} {NN+}", t):
        x = choice(["dozens of ", "hundreds of ", "thousands of "])
        
        # We'll only look at matches that start with "a" or "an".
        # This indicates an object or a thing of which many can exist.
        # If the match starts with "the", it might indicate something unique,
        # like "the capital of Nairobi". It doesn't make sense to transform
        # it into "hundreds of capitals of Nairobi".
        if match.group(1).string.lower() not in ("a", "an"):
            continue
        
        # Include the adjective, if any.
        if match.group(2):
            x += match.group(2).string
            x += " "
            
        # Pluralize the group of nouns.
        x += pluralize(match.group(3).string)
        s = s.replace(match.group(0).string, x)
    return s

news = "Flights into Kenya's main airport have been suspended " + \
       "after a passenger plane crash-landed on the runway in " + \
       "the capital Nairobi."
       
print inflate(news)