# coding: utf-8

# This script mines Wikipedia to predict 
# age, gender and education level of celebrities.

from pattern.web import DOM
from pattern.web import Wikipedia
from pattern.web import plaintext

from pattern.db import date

import re

# ------------------------------------------------------------------------------------

def celebrities():
    """ Returns a list of celebrities from Wikipedia.
    """
    celebrities = set()
    w = Wikipedia(language="en")
    p = w.search("List of people on the cover of Rolling Stone", cached=True)
    s = p.plaintext()
    # Extract the links from this page, excluding links in the footnotes section,
    # or links to band names (we just want names of individuals).
    for section in p.sections:
        if section.parent and section.parent.title in ("Individuals",):
            for name in section.links:
                # Yes = * [Rob Zombie], musician and filmmaker
                # No  = * Mark White, bass guitarist for [Spin Doctors]
                if "* " + name in s:
                    celebrities.add(name)
    return celebrities

#print len(celebrities()) # Small errors (why is Blind Melon included?),
#print                    # but overall good results: 1000+ celebrities.
#
#for p in sorted(celebrities()):
#    print p
#
#print "Arnold Schwarzenegger" in celebrities()
#print "Justin Bieber" in celebrities()
#print "Britney Spears" in celebrities()

# ------------------------------------------------------------------------------------

PERSON, PLACE = "person", "place"

def isa(entity, type=PERSON):
    """ Returns True if the given entity is of the given type.
    """
    # - Wikipedia.search() returns a WikipediaArticle:
    #   http://www.clips.ua.ac.be/pages/pattern-web#wikipedia
    # - The article comes with the HTML source code.
    # - The article comes with a plaintext version (no HTML tags).
    # - We can count how many times a word occurs in the plain text
    #   (e.g., articles about cities don't often use "he" or "she").
    # - We can search the HTML parse tree with CSS selectors.
    #   (e.g., the HTML often has a <div class="infobox"> with interesting metadata).
    try:
        w = Wikipedia(language="en")
        p = w.search(entity, cached=True)
        t = DOM(p.src) # HTML parse tree
        s = p.plaintext()
        s = s.lower()
        s = s.replace(".", " ")
        s = s.replace(",", " ")
        s = s.replace("'", " ")
        s = s.replace('"', " ")
        n = s.count(" ") * 1.0 or 0.0 # approximate word count
    except:
        pass
    # A person is an entity with a biography, a birthdate, and
    # a life's description containing gender-specific pronouns
    # (e.g., Noam Chomsky, Arnold Schwarzenegger).
    if type == PERSON:
        if t(".infobox.biography"):
            return True
        if t(".infobox th:contains('born')"):
            return True
        if any("early life" in x.title.lower() for x in p.sections):
            return True
        if sum(s.count(" %s " % w) for w in ( "he", "his")) / n > 0.01: # 1% he
            return True
        if sum(s.count(" %s " % w) for w in ("she", "her")) / n > 0.01: # 1% she
            return True
    # A place is an entity with a geography and/or a population
    # (e.g., New York, Jupiter, Middle Earth).
    if type == PLACE:
        if t(".infobox.geography"):
            return True
        if t(".infobox th:contains('coordinates')"):
            return True
        if t(".infobox th:contains('location')"):
            return True
        if t(".infobox th:contains('population')"):
            return True
        if t(".infobox th:contains('orbital period')"):
            return True
        if t("h2:contains('climate')"):
            return True
        if t("h2:contains('architecture')"):
            return True
        if any("geography" in x.title.lower() for x in p.sections):
            return True
        if any("flora" in x.title.lower() for x in p.sections):
            return True
        if any("fauna" in x.title.lower() for x in p.sections):
            return True
        if sum(s.count(" %s " % w) for w in (
          "city",
          "country",
          "house",
          "land",
          "location",
          "place",
          "room",
          "rooms",
          "space",
          "setting", 
          "town")) / n > 0.01:
            return True
    return False

#print isa("Uranus", PLACE)
#print isa("heaven", PLACE) # False; no coordinates, climate, flora, ...
#print isa("garden", PLACE)
#print isa("mosque", PLACE)
#print isa("bathroom", PLACE)
#print isa("Europe", PLACE)
#print isa("New York", PLACE)
#print isa("Belgium", PLACE)
#print isa("Coimbra", PLACE)
#print isa("Mount Vesuvius", PLACE)
#print isa("Middle Earth", PLACE)
#print isa("Minas Tirith", PLACE)
#print isa("Disneyland", PLACE)
#print isa("Mos Eisley", PLACE)
#print isa("Tatooine", PLACE)
#print isa("Lyonesse", PLACE)

#print isa("Lil' Bow Wow", PERSON)
#print isa("Arnold Schwarzenegger", PERSON)
#print isa("Xena", PERSON)
#print isa("Jesus", PERSON)
#print isa("T-800", PERSON) # True; ambiguous; actually is a robot.
#print isa("C-3PO", PERSON)
#print isa("Batman", PERSON)
#print isa("Batwoman", PERSON)

# ------------------------------------------------------------------------------------

def age(name):
    """ Returns the age of the given person.
    """
    # Use regular expression to try and parse 
    # a number of date formats from Wikipedia.
    try:
        w = Wikipedia(language="en")
        p = w.search(name, cached=True)
        t = DOM(p.src)
        s = plaintext(p.string)
        s = re.sub(r"\[[0-9]+\]", "", s)
        r = r"\(born ([0-9]+ [A-Za-z]+ )?([0-9]{4})\)" # (born 1 December 2000)
        x = t(".bday")
        y = t(".dday")
        x = x[0].content if x else re.search(r, s).group(2)
        y = y[0].content if y else str(date().year)
        x = plaintext(x)
        y = plaintext(y)
        x = x.split("-")[0] # YYYY-MM-DD
        y = y.split("-")[0]
        a = int(y) - int(x)
        return a
    except:
        pass
    try:
        r = ur"[A-Za-z]+ [0-9]+, ([0-9]{4})"
        r = ur"\(%s – %s\)" % (r, r) # (May 15, 1912 – October 7, 2003)
        x = re.search(r, s).group(1)
        y = re.search(r, s).group(2)
        a = int(y) - int(x)
        return a
    except:
        pass
    try:
        r = r"\(aged ([0-9]+)\)" # (aged 78)
        a = t(".infobox td:contains('aged')")
        a = a[0].content
        a = plaintext(a)
        a = re.search(r, a).group(1)
        a = int(a)
        return a
    except:
        pass
    return None

#print age("Britney Spears")
#print age("Vanilla Ice")
#print age("Nostradamus")
#print age("Douglas Hofstadter")

# ------------------------------------------------------------------------------------

def gender(name):
    """ Returns the gender of the given person (m/f).
    """
    try:
        w = Wikipedia(language="en")
        p = w.search(name, cached=True)
        s = plaintext(p.string)
        s = s.lower()
        s = s.replace("\n", "\n ")
        m = sum(s.count(" %s " % x) for x in ( "he", "his"))
        f = sum(s.count(" %s " % y) for y in ("she", "her"))
        g = m > f and "m" or "f" # More "he" or more "she"?
        return g
    except:
        return None

#print gender("Barack Obama")
#print gender("Michelle Obama")
#print gender("Mr. Tumnus")
#print gender("Galadriel")
#print gender("Falcor")
#print gender("Lassie") # conundrum
#print gender("C-3PO")

# ------------------------------------------------------------------------------------

def education(name, discrete=False, raw=False):
    """ Returns the education level of the given person (0.0-1.0).
    """
    try:
        w = Wikipedia(language="en")
        p = w.search(name, cached=True)
        t = DOM(p.src)
      # e = the percentage of links to articles about academic titles / achievements.
        e = [t("a[href*='%s']" % x) for x in (
            "academi"    , "academy_of" , "bachelor_of" , "college"     , 
            "degree"     , "doctor"     , "emeritus"    , "engineer"    , 
            "faculty"    , "fellow"     , "genius"      , "grandmaster" , 
            "institut"   , "invent"     , "master_of"   , "mathemati"   , 
            "phd"        , "ph.d"       , "physics"     , "professor"   , 
            "school_of"  , "scien"      , "student"     , "universi"    , 
            "valedictor" , 
        )]
        e = sum(map(len, e))
        e = e / float(len(t("a")))
        if raw:
            return e
        # Convert e to a human-interpretable range (0.0-1.0),
        # based on observations in the list of p people below,
        # i.e., Pattie Maes should be > 0.9, Miley Cirus < 0.5.
        e = max(e, 0.0)
        e = min(e, 1.0)
        m = {
            0.000: 0.40,
            0.003: 0.50,
            0.010: 0.60,
            0.020: 0.70,
            0.030: 0.80,
            0.060: 0.90,
            1.000: 1.00
        }
        for x, y in zip(sorted(m), sorted(m)[1:]):
            if y > e:
                e = m[x] + (m[y] - m[x]) * (e - x) / (y - x)
                break
        # With discrete=True, returns "+" or "-".
        e = e if not discrete else ("-", "+")[e > 0.01]
        return e
    except:
        return None

#                             # A   G   EDU (raw score)
p = (
    "Margaret Boden",         # 78  f   0.2745
    "Walter Daelemans",       # 54  m   0.1944
    "Pattie Maes",            # 53  f   0.1687
    "Peter Higgs",            # 85  m   0.1463
    "Elizabeth Blackburn",    # 66  f   0.1160
    "Etienne Vermeersch",     # 80  m   0.0952
    "Jane Goodall",           # 80  f   0.0826
    "Albert Einstein",        # 76  m   0.0803
    "Nijat Abasov",           # 19  m   0.0800 (chess)
    "Douglas Hofstadter",     # 69  m   0.0777
    "Carl Sagan",             # 62  m   0.0743
    "Richard Dawkins",        # 73  m   0.0704
    "Noam Chomsky",           # 86  m   0.0617
    "Larry Page",             # 41  m   0.0612 --------------------------- 90
    "Arthur Berger",          # 91  m   0.0533 (composer)
    "Laura Shields",          # 30  f   0.0455 (model / Mensa)
    "Ray Kurzweil",           # 66  m   0.0427
    "Godfried Danneels",      # 81  m   0.0354
    "Karl Sims",              # ??  m   0.0345 --------------------------- 80
    "Monica Lewinsky",        # 41  f   0.0251
    "Angela Merkel",          # 60  f   0.0210
    "Desiderius Erasmus",     # 70  m   0.0200
    "Jacob Aagaard",          # 41  m   0.0194 (chess)
    "Mark Zuckerberg",        # 30  m   0.0182
    "Leonardo Da Vinci",      # 67  m   0.0169 (informal education)
    "Jerry Springer",         # 70  m   0.0167
    "Emma Watson",            # 24  f   0.0118
    "Dolph Lundgren",         # 57  m   0.0117 (MA chemistry)
    "George W. Bush",         # 68  m   0.0100 --------------------------- 60
    "Jamie Oliver",           # 39  m   0.0097
    "Sarah Palin",            # 50  f   0.0089
    "Nicolas Sarkozy",        # 59  m   0.0089
    "Norman Schwarzkopf",     # 78  m   0.0086
    "Sylvester Stallone",     # 68  m   0.0066
    "Michael Jordan",         # 51  m   0.0066
    "Dizzee Rascal",          # 29  m   0.0057
    "Liv Tyler",              # 37  f   0.0056
    "Arnold Schwarzenegger",  # 67  m   0.0046
    "Madonna Ciccone",        # 56  f   0.0037 --------------------------- 50
    "Britney Spears",         # 33  f   0.0032
    "Miley Cirus",            # 22  f   0.0012
    "David Beckham",          # 39  m   0.0004
    "Victoria Beckham",       # 40  f   0.0000
    "Vanilla Ice",            # 47  m   0.0000
    "Snoop Dogg",             # 43  m   0.0000
    "Justin Bieber",          # 20  m   0.0000
    "Piet Huysentruyt",       # 52  m   0.0000
    "Regi Penxten",           # 38  m   0.0000
    "Josje Huisman",          # 28  f   0.0000
    "Jean-Marie Pfaff",       # 61  m   0.0000
)

#for p in p:
#    print p
#    print isa(p, PERSON)
#    print age(p)
#    print gender(p)
#    print education(p, discrete=False, raw=False)
#    print

# ------------------------------------------------------------------------------------

from pattern.en import referenced

q = "Vanilla Ice"
print q, "is", age(q), "years old"

q = "Lil' Bow Wow"
print q, "is a", {"m": "man", "f": "woman"}[gender(q)]

q = "Miley Cirus"
print q, "is", "smart" if education(q) > 0.5 else "an idiot"
