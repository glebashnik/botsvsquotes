from pattern.en import wordnet
from pattern.en import parsetree, conjugate
from random import choice

# WordNet is a lexical database of words linked to synonyms.
# http://www.clips.ua.ac.be/pages/pattern-en#wordnet

# For example:

for s in wordnet.synsets("soul"):
    print s.synonyms
    print s.gloss
    print
    
# Other relations include hypernyms (categories) and hyponyms (examples):

s = wordnet.synsets("soul")[0]
print s
print s.hypernym
print s.hyponyms()
print

# We can play around with this network, for example
# by randomly moving up and down the hypernyms and hyponyms.

def shift(noun):
    """ Returns a (random hyponym, description)-tuple for the given noun.
    """
    s = wordnet.synsets(noun)
    s = s[0]
    h = choice(s.hyponyms(recursive=True) or [s])
    return [h.synonyms[0], h.gloss]
    
print shift("soul")
print
# ["poltergeist", "a ghost that announces its presence with rapping and the creation of disorder"]

def alliterate(noun, head=2, tail=1):
    """ Returns an iterator of adjectives 
        whose head (prefix) and tail (suffix) match the given noun.
    """
    for a in wordnet.ADJECTIVES.keys():
        if noun[:head] == a[:head] and noun[-tail:] == a[-tail:]:
            yield a
            
print list(alliterate("poltergeist", head=3))
print
# polyglot poltergeist
# polyvalent poltergeist
# politically correct poltergeist
            
def drivel(noun):
    """ Generates drivel by shifting nouns in the description of the shifted noun,
        and prepending random alliterative adjectives.
    """
    drivel = []
    description = shift(noun)[1]
    description = description.split(";")[0]
    for sentence in parsetree(description):
        for i, w in enumerate(sentence.words):
            w, tag = w.string, w.tag
            if tag in ("VBD", "VBZ"):
                w = conjugate(w, "infinitive")
                w = conjugate(w, "past")
            if tag == "NN": # noun
                try:
                    w = shift(w)[0]
                    a = list(alliterate(w))
                    if a:
                        if i > 0 and sentence.words[i].tag == "JJ": # adjective
                            drivel.pop()
                        drivel.append(choice(a))
                except:
                    pass
            drivel.append(w)
    return " ".join(drivel)

print "poetic drivel"
print "-------------"
print

for w in (
  "soul",        # the visible disembodied pointillist poltergeist of a dead King's Counsel
  "creativity",  # a knockabout knot of resources
  "machine"):    # any macho magneto that made ovarian overexploitation of genitourinary geothermal energy to do work
    print w.upper()
    print drivel(w)
    print
