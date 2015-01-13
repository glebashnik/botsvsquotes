# coding: utf-8

# Machine learning example.

from pattern.vector import NB, SVM, SLP
from pattern.vector import count, words, chngrams
from pattern.vector import kfoldcv, fsel

# Statistical machine learning is a branch of AI that can be used
# to learn the "type" of unknown things, based on a "training set" 
# of known things. For these known things, we already know the type, 
# and we have a description of each thing, called a "vector".
# A vector is a just Python dictionary of features and feature weights.

# ------------------------------------------------------------------------------------

# The simplest classification algorithm is Naive Bayes,
# but it works quite well with text.

# A trivial example with animal features:
nb = NB()
nb.train({"swim": 1, "fin": 2, "legs": 0, "wings": 0}, type="fish")
nb.train({"swim": 0, "fin": 0, "legs": 1, "wings": 2}, type="bird")
nb.train({"swim": 1, "fin": 0, "legs": 4, "wings": 0}, type="mammal")

print nb.classify({"legs": 4})
print

# ------------------------------------------------------------------------------------

# For text, usually the word order is discarded in favor of word count.
# This is called a "bag-of-words" model, i.e., we count each word in a
# document. We can then compare it to other documents to see if they
# have frequent words in common. If so, they probably belong to the 
# same class or type.

# For example, if we have 10,000 product reviews + star rating,
# we can transform each review to a vector of adjective => count,
# use the star rating as vector type (e.g., * = -1, ***** = +1),
# and use this training set to predict the star rating of other reviews.

# Machine learning has been successfully applied to a number of
# text classification problems, e.g., spam detection,
# language identification, word type prediction (part-of-speech tagging),
# predicting the author's age and gender, predicting emotion in opinion,
# and so on.

def v(s):
    """ Returns a bag-of-words vector for the given string.
    """
    v = {}
    v.update(count(words(s)))
    return v
    
train = (
    ("cat", "A cat has whiskers"),
    ("cat", "A cat says meow"),
    ("cat", "the animal was purring softly"),
    ("dog", "A dog is an animal that says woof"),
    ("dog", "Why is that dog still barking?"),
    ("dog", "He happily wagged his tail")
)

# A robust, all-round classification algorithm is SVM.
# If SVM doesn't work on your machine, use SLP (= simple neural net).
classifier = SVM() 
for name, s in train:
    classifier.train(v(s), type=name)
    
print classifier.classify(v("the animal is purring and meowing"))
print classifier.classify(v("woof!"))
print

# ------------------------------------------------------------------------------------

# Vectors can be constructed in many different ways;
# what features you include will influence how accurate the classifier is.
# For example, in the example above there is no way to match "barking" to "bark"
# (for the classifier they are different words).
# A good strategy is to use character n-grams as features:
# sequences of n successive characters (usually n=3).
# The vector for the word "bark" then becomes: {"bar":1, "ark":1}
# Tne vector for the word "barking" becomes: {"bar":1, "ark":1, "rki":1, "kin":1, "ing":1}
# The two vectors now have overlap on 2 features ("bar" and "ark").
# This way, we can capture a lot of morphology, use of prepositions,
# use of punctuation marks, etc.

def ngram_vector(s, n=3):
    v = {}
    v.update(chngrams(s.lower(), n))
    return v

# ------------------------------------------------------------------------------------

# Here is an example more tuned to CC purposes.
# Take a look at veale/noc.py
# Take a look at tweets.py
# We've combined the two scripts to mine tweets about heroes and villains
# (you'll need the parse() function from noc.py):

# from pattern.web import Twitter
# from pattern.db import Datasheet, pd
# 
# noc = parse(pd("Veale's The NOC List.xlsx"))
# csv = Datasheet()
# 
# t = Twitter(language="en")
# for r in noc:
#     name = r["Character"]
#     alignment = None
#     if "Hero" in r["Category"]:
#         alignment = "good"
#     if "Villain" in r["Category"]:
#         alignment = "evil"
#     if alignment:
#         print name, alignment
#         for i in range(4):
#             for tweet in t.search(name, start=i, count=100, cached=True):
#                 csv.append((name, alignment, tweet.text))
#             csv.save(pd("good-evil.csv"))

# The script produces "good-evil.csv", a dataset of 18,000+ tweets
# of which we know that people are discussing a good or an evil character.
# We can use it as training material to create a classifier that predicts
# good or evil for tweets that mention unknown characters.

# First we prepare the training data:

import re

URL = re.compile(r"https?://[^\s]+")           # http://www.emrg.be
REF = re.compile(r"@[a-z0-9_./]+", flags=re.I) # @tom_de_smedt

from pattern.db import Datasheet, pd

train = []
for name, alignment, tweet in Datasheet.load(pd("good-evil.csv")):
    tweet = URL.sub("http://", tweet) # Anonymize URLs.
    tweet = REF.sub("@friend", tweet) # Anonymize usernames.
    train.append((ngram_vector(tweet, 5), alignment))
    
# ------------------------------------------------------------------------------------

# Let's look at the statistical accuracy of the classifier:
print kfoldcv(SVM, train, folds=3)
print

# This returns an (accuracy, precision, recall, F1-score, stdev)-tuple.
# The F1-score is the most important.
# An SVM trained on our data would be 94.6% accurate in knowing good from evil
# (this is a suspiciously high accuracy).

# ------------------------------------------------------------------------------------

classifier = SVM(train)

print classifier.distribution
print
# This reveals that there are 13,000 good tweets, and 5,000 evil tweets.
# This means the classifier is biased to predict "good",
# which probably influences the accuracy.

# ------------------------------------------------------------------------------------

# The following analysis gives us some insight in
# what features are most predictive:
for feature, predictivity, class_bias in fsel(train, top=100):
    print feature, predictivity, class_bias
print

# If you look at those features, you'll see that the classifier
# is mainly *memorizing* names of characters 
# (e.g., " bond"=good, " bilb"=good, " dart"=evil, " hutt"=evil, ...)
# So we've probably created an alignment-by-name detector,
# not an alignment-by-language-use detector.

# The actual accuracy can only really be tested if we have 
# an out-of-domain test dataset. For example, tweets about 
# politicians, that have been manually tagged as good or evil 
# by an expert group.

# ------------------------------------------------------------------------------------

# In any case, if somebody online has said that "Darth Vader is a thug",
# the classifier should have a pattern that recognizes 
# any "X is a thug" statement too.

for name, tweet in (
  (        "50 Cent", "50 Cent is a thug"                                ),
  (   "Miley Cirus", "Miley Cirus is a moron"                            ),
  (   "The Beatles", "The Beatles rock"                                  ),
  (         "Jesus", "Jesus is my hero"                                  ),
  (    "Tony Veale", "Tony Veale's work is inspiring"                    ),
  (  "Tom De Smedt", "Tom De Smedt's software kicks ass"                 ),
  (    "terrorists", "I don't understand the Charlie Hebdo terrorists"   ),
  (     "PJ Harvey", "PJ Harvey received an honorary doctorate"          ),
  ("George W. Bush", "George W. Bush is a dangerous dumbass"             ),
  (       "Cthulhu", "Cthulhu for president. Why vote for a lesser evil?")):
    print name, classifier.classify(ngram_vector(tweet, 5)).upper()
