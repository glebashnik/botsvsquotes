# coding: utf-8

from pattern.graph import Graph

from pattern.db import Datasheet, pd

from pattern.web import Google, plaintext

from pattern.search import search

# ------------------------------------------------------------------------------------

# This example demonstrates a semantic network of common sense.
# A semantic network is a graph where nodes represent concepts
# and edges (= connections between nodes) represent semantical
# relations (e.g., "is-a", "is-part-of", "is-property-of", ...)

# The data was collected manually and consists of about 10,000
# triples (concept1 -> relation -> concept2).
# The visual tool for adding new triples is online at:
# http://nodebox.net/perception

# The data is bundled in Pattern as a .csv file.

from pattern.graph import MODULE # path to pattern/graph/commonsense.csv
data = pd(MODULE, "commonsense.csv")
data = Datasheet.load(data)

# Create the graph:

g = Graph()
for concept1, relation, concept2, context, weight in data:
    g.add_node(concept1)
    g.add_node(concept2)
    g.add_edge(concept1, concept2, type=relation, weight=min(int(weight) * 0.1, 1.0))

# ------------------------------------------------------------------------------------

# The halo of a node is a semantical representation of a concept.
# The halo is made up of other concepts directly or indirectly related to this concept,
# defining it. 

# For example:
#
# - Darth Vader is-a Sith
# - Darth Vader is-part-of Death Star
# - evil is-property of Darth Vader
# - black is-property-of Darth Vader
# - hoarse is property-of Darth Vader
# ...
# The concepts villain, Death Star, evil, black, hoarse are all in the concept halo
# of Darth Vader. They define what Darth Vader is.

# Each Node object has a Node.flatten() method that returns a list of nodes.
# With depth=1, the list contains the node itself.
# With depth=2, the list contains the node and directly connected nodes.
# ...
# Increasing the depth is called "spreading activation".
# http://www.clips.ua.ac.be/pages/pattern-graph#node

def halo(node, depth=2):
    """ Returns the halo of the given node as a list of nodes.
    """
    return node.flatten(depth)

print
print "Darth Vader's halo:"
print "-------------------"

for n in halo(g["Darth Vader"]):
    print n.id

# To visualize the Darth Vader halo,
# we can use the canvas.js visualization engine bundled in Pattern.

# A Graph object has a Graph.export(folder_name) method that
# creates a new folder with HTML and canvas.js JavaScript code.
# http://www.clips.ua.ac.be/pages/pattern-graph#canvas

# A Graph object has a Graph.copy(nodes=[]) method that returns
# a new graph, containing only the nodes in the given list and
# the edges between them. 

# We can then combine halo(), Graph.copy() and Graph.export():

g.copy(nodes=halo(g["Darth Vader"])).export(pd("Darth_Graph"))

# Open the index.html in the generated folder in a browser!

# ------------------------------------------------------------------------------------

# The semantic field of a node roughly means: 
# every node that has the given node as its type.
# For example, the semantic field of "animal" is "bird", "fish", "rabbit", "albatross", ...
# Note that "albatross" is a more specific version of "bird",
# so we will need to use a spreading activation technique to find them all.

# The Node.flatten() method can also be called with a user-defined function.
# This function decides if an edge should be "followed" during the spreading
# activation. In this case, we only want to follow edges of type "is-a".

# The Graph.fringe() method returns a list of nodes that are on the rim of the graph.
# With depth=1, the list contains nodes that have only 1 edge.
# With depth=2, the list contains nodes with 1 or 2 edges.
# ...

# So: with Node.flatten() we can map the entire "is-a" tree of a node
# (this is called a "taxonomy") and with Graph.fringe() we could select
# the "leaves" of that tree. We can play around with the parameters
# of the field() function below, but generally depth=3 and fringe=2
# gives useful / interesting results..

def field(node, depth=3, fringe=2):
    """ Returns the semantic field of the given node as a list of nodes.
    """
    def traversable(node, edge):
        return edge.node2 == node and edge.type == 'is-a'
    g = node.graph.copy(nodes=node.flatten(depth, traversable))
    g = g.fringe(depth=fringe)
    g = [node.graph[n.id] for n in g if n != node]
    return g

print
print "Semantic field of the concept 'animal':"
print "---------------------------------------"

for n in field(g["animal"]):
    print n.id

# ------------------------------------------------------------------------------------

# The PROPERTIES dict contains every concept1 in "concept1 is-property-of concept2"
# triples: "evil", "black", "hoarse", ...  The reason that we use a dict instead of 
# a list is that it is faster for looking up.

PROPERTIES = [e.node1.id for e in g.edges if e.type == 'is-property-of']
PROPERTIES = dict.fromkeys(PROPERTIES, True)

# ------------------------------------------------------------------------------------

# The properties() function returns a list of nodes that are properties of the given node.
# More specifically, the list contains properties that fall in the halo of the given node.
# This way, nodes that have few edges (in other words they aren't well described
# in the data set) can "borrow" properties from surrounding nodes,
# so we have a little more knowledge to work with.

# Preferably, we want the more interesting properties at the start of the list
# (the list can be very long). 

# As a measure of interestingness, we use betweeness centrality 
# (Brandes' Betweenness Centrality algorithm).

# This of course is only one of many possible approaches.
# Betweenness centrality is a score for each node that represents 
# how much traffic (= shortest paths between other nodes) passes through a node.
# Nodes that have high traffic have a higher score.
# We can use the Node.centrality value (0.0-1.0) to sort the list of properties.

cache = {} # Cache results for faster reuse.

def properties(node):
    """ Returns a list of nodes that are properties of the given node,
        sorted by betweenness centrality.
    """
    if node.id in cache:
        return cache[node.id]
    g = node.graph.copy(nodes=halo(node))
    p = (n for n in g.nodes if n.id in PROPERTIES)
    p = reversed(sorted(p, key=lambda n: n.centrality))
    p = [node.graph[n.id] for n in p]
    cache[node.id] = p
    return p

print
print "Properties of Darth Vader:"
print "--------------------------"

for n in properties(g["Darth Vader"]):
    print n.id

# ------------------------------------------------------------------------------------

# We can now compare how similar two nodes are, based on the properties they share.
# If two nodes don't share any properties (this is more likely than not),
# we can compare them by the distance between their properties.
# For example, the dataset might contain "evil is-property-of Darth Vader",
# "malicious is-property-of Jabba the Hut" and "sensitive is-property-of Luke".
# Obviously, the distance between "evil" and "malicious" will be shorter
# (most likely they will be directly connected with a "evil is-related-to malicious").

# The Graph.shortest_path() method returns a list of nodes that lie along 
# the shortest possible route between two given nodes
# (Dijkstra's shortest path algorithm)

# It takes an optional, user-defined function that can be used to promote
# or discourage certain edges. In this case, we discourage all edges
# except "is-property-of edges" (so routes along properties will always be preferred).

def similarity(node1, node2, k=3):
    g = node1.graph
    h = lambda id1, id2: 1 - int(g.edge(id1, id2).type == 'is-property-of')
    w = 0.0
    for p1 in properties(node1)[:k]:
        for p2 in properties(node2)[:k]:
            p = g.shortest_path(p1, p2, heuristic=h)
            w += 1.0 / (p is None and 1e10 or len(p))
    return w / k

print
print "What is similar to Darth Vader?"
print "-------------------------------"

print "A bat?", similarity(g["Darth Vader"], g["bat"])
print "A bunny?", similarity(g["Darth Vader"], g["bunny"])
print "A teapot?", similarity(g["Darth Vader"], g["teapot"])

# The most similar of these three is the bat,
# because its properties (is black, related to evil) 
# are similar to those of Darth Vader.

# To get a full analysis, you'd need to hack into the similarity()
# to examine the shortest paths between nodes.

# ------------------------------------------------------------------------------------

# The nearest_neighbors() function simply takes a node and a list of candidate nodes,
# and returns the list of candidates sorted by similarity.

def nearest_neighbors(node, candidates=[], k=3):
    """ Returns the list of candidate nodes sorted by similarity.
    """
    w = lambda n: similarity(node, n, k)
    return sorted(candidates, key=w, reverse=True)
    
# This is interesting because we can use semantic fields as candidates.
# For example, what person is most similar to Darth Vader?
# This can take some time to compute (winners are H. P. Lovecraft and Adolf Hitler).

print
print "What persons are most similar to Darth Vader?"
print "---------------------------------------------"

for node in nearest_neighbors(g["Darth Vader"], field(g["person"]))[:10]:
    print node.id
    
print
print "What are creepy animals?"
print "------------------------"

for node in nearest_neighbors(g['creepy'], field(g['animal']))[:10]:
    print node.id
    
# Some of the results are the result of manual annotation.
# In other words, a person said that "creepy is-property-of octopus".
# But results like "mole" and "Sleipnir" are interesting,
# because they are inferred from common sense reasoning based on similar properties.

# ------------------------------------------------------------------------------------

# Here is a possible approach to expand the semantic network automatically
# (based on Veale's simile approach).

# You'll need a Google license key to make this work.
# Read more here: http://www.clips.ua.ac.be/pages/pattern-web#services

def learn(concept):
    """ Returns a list of properties for the given concept,
        collected from a "I think X is Y".
    """
    q = 'I think %s is *' % concept
    p = []
    g = Google(language='en', license=None)
    for i in range(10):
        for result in g.search(q, start=i, cached=True):
            m = plaintext(result.description)
            m = search(q, m) # Use * as a wildcard.
            if m:
                p.append(m[0][-1].string)
    return [w for w in p if w in PROPERTIES] # only handles known properties...

#print learn("Justin Bieber")
