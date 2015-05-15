import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import requests
import pylab

# basic graph operations
G=nx.Graph()
G.add_nodes_from([1,2,3])
G.add_edges_from([(1,2),(1,3)])
G.add_node(4)
G.add_edge(1,4)
G.remove_node(4)
G.neighbors(1)

H = nx.path_graph(10)
H.nodes()
H.edges()

# info on edges
G.add_node(4)
G.add_edge(1, 4, weight=10, label='Rocky road to Dublin')
G[1][4]

G[1][3]['weight'] = 7
G[1][3]['label'] = 'Moderate way to Dublin'

G[1][2]['weight'] = 5
G[1][2]['label'] = 'Easy way to Dublin'

# support for Directed graphs, Multigraphs (MultiGraph) and Directed Multigraphs (MultiDiGraph)

# Analyzing graphs
nx.connected_components(G)

# Drawing graphs
nx.draw(G)

# generate and draw trees
btree = nx.balanced_tree(2,4)
pos=nx.graphviz_layout(btree,prog='dot')
nx.draw(btree,pos,with_labels=False,arrows=False)

circ_tree = nx.balanced_tree(3,5)
pos=nx.graphviz_layout(circ_tree,prog='twopi',args='')
nx.draw(circ_tree, pos, node_size=20,alpha=0.5,node_color="blue", with_labels=False)

# Data Structure: "dictionary of dictionaries of dictionaries" as the basic network data structure
G.adj
btree.adj

#-------------------Shortest path example---------------------------#

# generate random graph matrix
g_mat = np.random.binomial(1, 0.1, (10, 10))
G = nx.Graph(g_mat)

# add weights on the edges
weights = np.random.random_integers(low=1, high=10, size=len(G.edges()))
for i, (n1, n2) in enumerate(G.edges()):
    G[n1][n2]['weight'] = weights[i]

# drawing the graph
pos=nx.graphviz_layout(G,prog='dot')
nx.draw_networkx(G, pos)

# shortest path
path = nx.shortest_path(G, 3, 6, weight='weight')

def node_colors(G, path):
    colors = []
    for node in G.nodes():
        if node in path:
            colors.append('b')
        else:
            colors.append('r')
    return colors

colors = node_colors(G, path)
nx.draw_networkx(G, pos, node_color=colors)

# draw graph with weights on edges
edge_labels = {(n1,n2): G[n1][n2]['weight'] for (n1,n2) in G.edges()}
pylab.figure(1, figsize=(8, 8))
nx.draw_networkx(G, pos, node_color=colors)
nx.draw_networkx_edge_labels(G , pos, edge_labels=edge_labels)
pylab.show()

def draw_shortest_path(G, pos, start, end):
    path = nx.shortest_path(G, start, end, weight='weight')
    colors = node_colors(G, path)
    edge_labels = {(n1,n2): G[n1][n2]['weight'] for (n1,n2) in G.edges()}
    pylab.figure(1, figsize=(8, 8))
    nx.draw_networkx(G, pos, node_color=colors)
    nx.draw_networkx_edge_labels(G , pos, edge_labels=edge_labels)
    pylab.show()


#-----------------------Examples from networkx website-------------------------------------#

# Graph of Words example
# http://networkx.github.io/documentation/networkx-1.9.1/examples/graph/words.html
# generate_graph - from the above example
# words taken from: http://www-cs-faculty.stanford.edu/~uno/sgb-words.txt
GWords = generate_graph(words)
nx.shortest_path(GWords, 'chaos', 'order')
nx.shortest_path(GWords, 'geeks', 'smart')

# graphs to json example: http://networkx.github.io/documentation/networkx-1.9.1/examples/javascript/force.html

# pretty dump to json
json.dump(d, open('/home/mihai/work/networkx_presentation/networkx_to_js.json','w'),
            sort_keys=True, indent=4, separators=(',', ': '))

# Check more examples at: http://networkx.github.io/documentation/networkx-1.9.1/examples/index.html


#-----------------------Simulating civilisations----------------------------------------------#

# inspired from http://timotheepoisot.fr/2012/05/18/networkx-metapopulations-python/

class Patch:
    def __init__(self, label, status='w', pos=(0,0)):
        self.status = status
        self.pos = pos
        self.label = label

    def __str__(self):
        return(str(self.label))

    def __repr__(self):
        return(str(self.label))

    def __hash__(self):
        return hash(self.label)

    def __eq__(self, other):
        return self.label == other.label


class Simulation(object):
    nr_patches = 100   # Number of patches
    c_distance = 15  # An arbitrary parameter to determine which patches are connected

    def __init__(self, with_history=True):
        self.civs = [{'color': 'r'}, {'color': 'b'}, {'color': 'y'}]
        self.step = 0
        self.patches = []
        self.history = []
        self.with_history = with_history

        self.graph = nx.Graph()
        # generate positions in 2d space for patches
        positions = np.random.uniform(high=100, size=(self.nr_patches,2))
        # add patches to the graph
        for i in range(self.nr_patches):
            patch = Patch(label=i, pos=positions[i])
            self.graph.add_node(patch)
            self.patches.append(patch)
        # add edges
        for p1 in self.graph.nodes():
            for p2 in self.graph.nodes():
                if p1 == p2:
                    continue
                dist = np.sqrt((p1.pos[1]-p2.pos[1])**2+(p1.pos[0]-p2.pos[0])**2)
                if dist <= self.c_distance:
                    self.graph.add_edge(p1,p2)

        # place civilisations
        civ_posistions = np.random.random_integers(low=0, high=self.nr_patches,
                                            size=(len(self.civs),))
        for i, civ_pos in enumerate(civ_posistions):
            # each civ will have 3 neighboring patches
            civ_patch = self.patches[civ_pos]
            civ_patch.status = self.civs[i]['color']
            self.civs[i]['patches'] = set([civ_patch])
            civ_counter = 1
            for civ_ngb in self.graph[civ_patch]:
                # choose neighbors that are not already taken
                if civ_ngb.status != 'w':
                    continue
                civ_ngb.status = self.civs[i]['color']
                self.civs[i]['patches'].add(civ_ngb)
                civ_counter += 1
                if civ_counter > 2:
                    break

        # keep track of changes in history
        if self.with_history:
            self.save_history()

    def run_simulation(self, steps=1):
        for step in range(steps):
            # do actions for each civ
            for civ in self.civs:
                # for each node a civ will try to expand to the neighbors
                # at each step only one attempt to conquer a patch can be made
                attempts = set()
                conquered = set()
                for patch in civ['patches']:
                    for neighbor in self.graph[patch]:
                        # make sure this civ doesn't own the patch already
                        if neighbor.status == civ['color']:
                            continue
                        # an attempt was already made this turn
                        if neighbor in attempts:
                            continue
                        # try to conquer the patch
                        result = self.conquer(neighbor, civ)
                        attempts.add(neighbor)
                        if result:
                            if neighbor.status != 'w':
                                # the patch belongs to another civ
                                other_civ = self.get_civ_by_color(neighbor.status)
                                other_civ['patches'].remove(neighbor)
                            conquered.add(neighbor)
                # claim conquered patches
                for patch in conquered:
                    patch.status = civ['color']
                    civ['patches'].add(patch)

            if self.with_history:
                self.save_history()
            self.step += 1

    def conquer(self, patch, civ):
        # total number of neighbors plus the node itself
        total = len(self.graph[patch]) + 1
        # number of neighbors belonging to this civ
        civ_ngbs = len([ngb for ngb in self.graph[patch]
                        if ngb.status == civ['color']])
        # random component
        return bool(np.random.binomial(1, float(civ_ngbs)/total))

    def get_civ_by_color(self, color):
        for civ in self.civs:
            if civ['color'] == color:
                return civ

    def save_history(self):
        self.history.append(
            {civ['color']: len(civ['patches']) for civ in self.civs})

    def draw_graph(self):
        pylab.figure(1, figsize=(8, 8))
        nx.draw(self.graph, {patch: patch.pos for patch in self.graph.nodes()},
                with_labels=True,
                node_color=[patch.status for patch in self.graph.nodes()])
        pylab.show()

    def draw_history(self):
        time = range(1, len(self.history)+1)
        args = []
        for civ in self.civs:
            args.append(time)
            args.append([h[civ['color']] for h in self.history])
            args.append(civ['color'])
        kwargs = {'figure': pylab.figure(2, (8,8))}
        pylab.plot(*args, **kwargs)
