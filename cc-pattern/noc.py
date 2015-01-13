from pattern.db import pd

# --- EXCEL PARSER -------------------------------------------------------------------
# A very simple Excel-file parser, based on:
# http://stackoverflow.com/questions/4371163/reading-xlsx-files-using-python

CELLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def xlsx(path):
    """ Returns a list of rows, where each row is a list of column values.
    """
    import zipfile
    from xml.etree.ElementTree import iterparse
    a = []
    r = {}
    v = ""
    z = zipfile.ZipFile(path)
    s = [e.text for x, e in iterparse(z.open("xl/sharedStrings.xml")) if e.tag.endswith("}t")]
    for x, e in iterparse(z.open("xl/worksheets/sheet1.xml")):
        if e.tag.endswith("}v"): # <v>84</v>
            v = e.text
        if e.tag.endswith("}c") \
         and e.attrib.get("t"):  # <c r="A3" t="s"><v>84</v></c>
            v = s[int(v)]
        if e.tag.endswith("}c"):
            c = e.attrib["r"]    # AZ22
            c = c.rstrip("0123456789")
            r[c], v = v, ""
        if e.tag.endswith("}row"):
            if any(r.values()):  # skip empty rows
                a.append(r)
            r = {}
    m = max([max(r.keys()) for r in a])
    for i, r in enumerate(a):    # fill empty cells
        for c in CELLS.split(m)[0] + m:
            r.setdefault(c, "")
        a[i] = [r[c] for c in sorted(r)]
    return a
    
#noc = xlsx(pd("Veale's The NOC List.xlsx"))

# [["Character"        , "Gender" , "Address 1"          ],
#  ["Daniel-Day Lewis" , "male"   , "Sugarloaf Mountain" ],
#  ["Tina Fey"         , "female" , "Rockerfeller Center"]
# ]

# --- HELPERS ------------------------------------------------------------------------
# Helper tools for parsed Excel files.
#
# 1) The Excel parser returns a list of rows, where each row is a list of column values.
#    It would be more useful if we had a list of dicts,
#    so we can say row["Gender"] instead of row[1],
#    This is what the assoc() function does.
#
# 2) Sometimes we want all the values in a certain column.
#    This is what the col() function does.
#
# 3) Sometimes column values are comma-separated enumerations.
#    For example, "Positive Talking Points" => "rich, naive".
#    It would be handy if we could get these as a list: ["rich", "naive"].
#    This is what the split() function does.
#
# 4) If many values in a column are like this,
#    the column is most likely splitable().
#
# 5) Often we will need indexes, i.e., a dict with keys that point to rows.
#    For example: a dict of unique character names,
#    where each name points to the relevant row.
#    Or a gender dict with keys "male" and "female",
#    where gender_dict["male"] is a list of all male rows.
#    This is what the index() function does.

# 6) To get insight into the data set,
#    we may want to know the frequency of values.
#    For example, "how many rows in the data set are female?".
#    This is what the freq() function does.

def assoc(rows):
    """ Returns an iterator of rows, where each row is a dict of (header, value)-items.
    """
    headers = rows[0]
    for r in rows[1:]:
        r = dict((headers[i], v) for i, v in enumerate(r))
        yield r

#noc = list(assoc(xlsx(pd("Veale's The NOC List.xlsx"))))

# [{"Character": "Daniel-Day Lewis", 
#      "Gender": "male", 
#   "Address 1": "Sugarloaf Mountain"
#  },
#  {"Character": "Tina Fey", 
#      "Gender": "male", 
#   "Address 1": "Rockerfeller Center"
#  },
# ]

def col(rows, key):
    """ Returns an iterator of values in the given column.
        For a list of lists, the given key is a number (index).
        For a list of dicts, the given key is a string.
    """
    for r in rows:
        yield r[key]

#rows = [["Daniel", "m"], ["Tina", "f"]]
#print list(col(rows, 1)) # ["m", "f"]

def split(v, separator=","):
    """ Returns the given string as a list.
    """
    return [x.strip() for x in v.split(separator)]

#print split("funny, entertaining", ",") # ["funny", "entertaining"]

def splitable(col, separator=",", threshold=1):
    """ Returns True if (some of) the values are strings that contain the separator.
    """
    i = 0
    for v in col:
        if isinstance(v, basestring) and separator in v:
            i += 1
        if i >= threshold:
            return True
    return False

def index(rows, key, unique=True):
    """ Returns a dict of (value for key, row)-items.
        With unique=False, returns a dict of (value for key, [row1, row2, ...])-items.
    """
    m = {}
    for r in rows:
        k = r[key]
        if not isinstance(k, list):
            k = [k]
        for k in k:
            if not unique:
                m.setdefault(k, []).append(r)
            else:
                m[k] = r
    return m

#rows = [["Daniel", "m"], ["Tina", "f"], ["Abraham", "m"]]
#print index(rows, 1, unique=False) # {"m": [["Daniel", "m"], ["Abraham", "m"]], 
                                    #  "f": [["Tina", "f"]]}

def freq(col, top=10):
    """ Returns a sorted list of (count, value)-tuples for values in the given list.
        The list is truncated to the top most frequent values.
    """
    f = {}
    for v in col:
        if not isinstance(v, list):
            v = [v]
        for v in v:
            if v not in f:
                f[v] = 0
            f[v] += 1
    f = f.items()
    f = sorted(((count, v) for v, count in f), reverse=True)
    return f[:top]

# ------------------------------------------------------------------------------------

NOC = "Veale's The NOC List.xlsx"
# Character, Gender, Address 1, Address 2, Address 3, Politics, Marital Status, 
# Opponent, Typical Activity, Vehicle of Choice, Weapon of Choice, Seen Wearing,
# Domains, Genres, Fictive Status, Portrayed By, Creator, Creation, Group Affiliation,
# Fictional World, Category, Negative Talking Points, Positive Talking Points

def parse(path):
    # 1) Parse the Excel sheet at the given path (xlsx()).
    # 2) Map the list of lists to list of dicts (assoc()).
    # 3) If a column contains splitable values (e.g., "1,2,3"),
    # 4) split the values in the column.
    rows = list(assoc(xlsx(pd(path)))) # 1 + 2
    for k in rows[0].keys():
        if splitable(col(rows, k)):    # 3
            for r in rows:
                r[k] = split(r[k])     # 4
    return rows

# ------------------------------------------------------------------------------------
# Examples of use.

noc = parse(NOC)

print "How many characters are in the NOC list?"
print "----------------------------------------"
print len(noc)
print
# +- 800

print "What is the distribution of political views in the NOC list?"
print "------------------------------------------------------------"
print freq(col(noc, "Politics"))
print

print "Which characters wear a hat?"
print "----------------------------"
for r in noc: # {"Character": "Daniel Day-Lewis", "Seen Wearing": ["stove-pipe hat"]}
    for v in r["Seen Wearing"]:
        if "hat" in v:
            print r["Character"]
            break
print
# Abraham Lincoln, Jack Sparrow, ...

print "Which characters are astronauts?"
print "--------------------------------"
jobs = index(noc, "Category", unique=False)
for r in jobs["Astronaut"]:
    print r["Character"]
print
# Buzz Aldrin, Mr. Spock, ...

print "Which characters are ugly?"
print "--------------------------"
traits1 = index(noc, "Positive Talking Points", unique=False)
traits2 = index(noc, "Negative Talking Points", unique=False)
traits = {}
traits.update(traits1)
traits.update(traits2)
for r in traits["ugly"]:
    print r["Character"]
print
# Jabba the Hutt, Freddy Krueger, ...

print "What do rich people wear?"
print "-------------------------"
clothes = []
for r in traits["rich"]:
    clothes.append(r["Seen Wearing"])
for x in freq(clothes):
    print x
print
# sharp suit, three-piece suit, ...

print "What do bad guys do?"
print "--------------------"
seen = set()
activities = []
for k in traits:
    if k in ("cruel", "sadistic", "cold", "traitorous"):
        for r in traits[k]:
            if r["Character"] not in seen:
                # Multiple traits may point to a character,
                # so we need to make sure we don't count it twice.
                seen.add(r["Character"])
                activities.append(r["Typical Activity"])
for x in freq(activities):
    print x
print
# devise evil schemes, backstabbing, ...

print "What are the most common properties in the NOC list?"
print "----------------------------------------------------"
properties = []
for r in noc:
    for p in r["Positive Talking Points"]:
        properties.append(p)
    for p in r["Negative Talking Points"]:
        properties.append(p)
for count, p in freq(properties, top=25):
    print count, "\t", p
print
