# coding: utf-8

from pattern.web import URL, DOM, plaintext

# This script generates tropes.csv.

# Tropes are things like a plot twist, a premise, a tic,
# that make a story (e.g., movie, book) more interesting.
# For example: Flexing The Neck Muscles before a fight,
# an Alien Invasion, the Wild West, the Dumbass Has a Point, etc.
# Tropes are the creative product of the writers.
# This kind of knowledge might be interesting for CC purposes.

# There is an online collection of tropes at:
# http://tvtropes.org/

# This script uses CSS Selectors to mine tvtropes.org.
# A CSS Selector is a kind of search query that selects
# specific pieces from a HTML web page.
# For example: "all <a> links that occur in a <li> list",
# or "texts that occur in <p class="review"> paragraphs".
# This kind of script is called a "crawler".

# Take a look at the index of tropes on this page:
# http://tvtropes.org/pmwiki/pmwiki.php/Main/Tropes

# The index is organized in a couple of categories (Narrative Tropes, Genre Tropes, ...), 
# each with links to subcategories (Narrative Tropes => Plots, Settings, ...),
# each with links to specific tropes (Plots => Alien Invasion, Everyone Meets Everyone, ...),
# each with links to movies and TV series (Alien Invasion => Stargate SG-1, ...)

# So, what we could do is write a script that:
# 1) visits the index and identifies links to tropes,
# 2) visits the linked trope pages and identifies links to movies,
# 3) visits the linked movie pages,
# etc.

# Take a look at the index of tropes again:
# http://tvtropes.org/pmwiki/pmwiki.php/Main/Tropes

# In the browser, enable the Developer Tools.
# For example, in Chrome: from the View menu > Developer > Developer Tools.

# We now get a view of the HTML source code. 
# The Developer Tools have a "magnifying glass" button,
# which allows us to hover over elements on the web page and inspect their HTML.
# We can then use Pattern to download the HTML source code, parse the HTML tree,
# and extract the portions that are interesting (e.g., links) with CSS Selectors:
# http://www.clips.ua.ac.be/pages/pattern-web#DOM

# If you don't know about CSS Selectors yet, be sure to read up on them.
# They are extremely useful for data mining.

def tropes():
    
    """ Returns an iterator of (trope, category, description, [movie1, movie2, ...]) tuples.
    """
    
    # Visit the index and download the HTML source code:
    url1 = URL("http://tvtropes.org/pmwiki/pmwiki.php/Main/Tropes")
    src1 = url1.download(cached=True)
    
    # Hm, there is a weird character in the HTML source that crashes the script.
    # Took a while to figure this out, but if we remove the character
    # the script runs fine:
    src1 = src1.replace("&#8212;", "--")
    
    # Parse the HTML tree.
    # This means that we will end up with a "dom" variable
    # that is a list of nested HTML elements (e.g., <head>, <body>),
    # each a nested list of other elements (e.g., <body> contains 
    # <h1> headers and <p> paragraphs of text), and so on.
    dom1 = DOM(src1)
    #print dom1.src
    
    # The HTML source has a <div id="wikitext"> with the main content.
    # Inside this <div> are <ul> bulleted lists that contain <a> links 
    # to trope categories (Plots, Settings, ...).
    # <div id="wikitext">
    #     <ul>
    #         <li><a href="...">Plots</a></li>
    #         <li><a href="...">Settings</a></li>
    #
    # Those are the links we want:
    for a1 in dom1("div#wikitext > ul li a"):
        category = plaintext(a1.content) # Plots, Settings, ...
        
        # Each <a> has a "href" attribute, for example
        # <a href="http://tvtropes.org/pmwiki/pmwiki.php/Main/Plots">Plots</a>
        # We'll now visit that link to get to the actual tropes:
        url2 = URL(a1.href)
        src2 = url2.download(cached=True, throttle=1)
        src2 = src2.replace("&#8212;", "--")
        dom2 = DOM(src2)
        
        # Notice the throttle=1.
        # This means that the script will wait 1 second before continuing.
        # If we are going to mine a lot of data from tvtropes.org,
        # we should raise the throttle to something like 60 seconds,
        # so we don't crash their server with automated requests from our script.
        # Set a high throttle, start the script, and take a nap.
        
        # Each category page has a <div id="wikitext"> that contains
        # <ul> bulleted lists with <a> links to tropes
        # (e.g., Plots => Alien Invasion, Everyone Meets Everyone, ...)
        # Those are the links we want:
        for a2 in dom2("div#wikitext > ul li a"):
            trope = plaintext(a2.content)
            
            # <a href="http://tvtropes.org/pmwiki/pmwiki.php/Main/AlienInvasion">Alien Invasion</a>
            # We'll now visit that page to get to the actual tropes:
            try:
                url3 = URL(a2.href)
                src3 = url3.download(cached=True, throttle=1)
                src3 = src3.replace("&#8212;", "--")
                dom3 = DOM(src3)
            except:
                continue
            
            # Each trope web page has a description and links to movies that feature the trope.
            # Let's extract the description; this is useful data we can use later on.
            try:
                description = dom3("div#wikitext")[0].content
                description = description[:description.find("<h1>Examples")]
                description = description[:description.find("<h2>Examples")]
                description = plaintext(description)
                description = description.strip()
            except:
                continue
            # It's difficult to extract the description,
            # since there aren't many HTML tags or CSS classes to hook into.
            # It's just a <div id="wikitext"> that contains text, sidebars, lists with links, ...
            # It would have been nicer if there was a clean <div class="description"> to extract.
            # For now, we just convert everything inside the <div id="wikitext"> to plain text,
            # without HTML tags, up to where it says <h2>Examples</h2>.

            # <div class="folderlabel">Films – Live Action</div>
            # <div class="folder">
            #     <ul>
            #         <li>
            #             <em><a href="...">Signs</a></em>
            #             <p>Signs: The aliens attempt a military invasion but are stopped 
            #                by their crippling vulnerability to water.
            #             </p>
            #         </li>
            examples =[]
            for example in dom3("div.folder > ul > li, .asscaps + ul > li"):
                
                # Actually, we don't know most of the Anime series or Tabletop Games they mention... 
                # Let's focus on examples of well-known Live-Action movies.
                # We can find out if an example is a live-action movie 
                # by sniffing the preceding <div class="folderlabel">:
                try:
                    x = example.parent # <ul>
                    x = x.parent       # <div class="folder">
                    x = x.previous     # <div class="folderlabel>"
                    x = plaintext(x.content)
                    x = x.strip()
                    x = x.lower()
                    x = x.replace("-", " ")
                    genre = x
                    if not "live action" in genre:
                        continue # = skip this one
                except:
                    continue
                
                # Since the content on tvtropes.org is written by many humans, 
                # the content is a little messy (i.e., not always what we expect).
                # The code below won't always work, so we brute-force it in a try-except block,
                # to prevent the entire script from crashing all of a sudden.
                # We'll just silently ignore exceptions and move on.
                try:
                    title = example("em a")[0]
                    title = plaintext(title.content)
                    example = plaintext(example)
                    examples.append(title)
                except:
                    continue
                    
            # We now have a category, trope, description and a list of examples.
            # We'll yield the data back to the user:
            yield (trope, category, description, examples)
            
            # What does "yield" mean?
            # Python functions can "return" a value.
            # For example, a number, a string or a list of values.
            # If it returns a list,
            # we can use a for-loop to iterate through all the values in the list.
            # A function that "yields" something is like returning a list,
            # only it will stop immediately when the user stops iterating
            # (i.e., it doesn't continue crawling tvtropes.org).

# Let's have a look at the first three results:
count = 0
for trope, category, description, examples in tropes():
    count += 1
    print trope.upper()
    print category
    print
    print description
    print
    print examples
    print 
    print "-------------------------------------"
    print
    if count >= 3:
        break

# The crawler seems to work pretty well.
# We can let it run for a while and store the results in a local database. 
# See tropes.csv, for 10,000+ tropes linked to live-action movies.

#from pattern.db import Datasheet, pd
#
#csv = Datasheet()
#
#count = 0
#for trope, category, description, examples in tropes():
#    if not examples:
#        continue
#    print trope
#    count += 1
#    csv.append((trope, "\n".join(examples), description))
#    if count % 25 == 0: # = update database every 100 new results
#        csv.save(pd("tropes.csv"))