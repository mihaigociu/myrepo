import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import requests

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


#-----------------------Simulating populations----------------------------------------------#
