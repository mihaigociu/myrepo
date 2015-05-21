import json
import networkx as nx
import numpy as np
from networkx.readwrite import json_graph

#-----------------------Simulating civilisations----------------------------------------------#

# inspired from http://timotheepoisot.fr/2012/05/18/networkx-metapopulations-python/

class Patch(object):
    def __init__(self, label, status='w', pos=(0,0)):
        self.status = status
        self.pos = pos
        self.label = label

    def toJSON(self):
        return int(self.label)

    def __str__(self):
        return(str(self.label))

    def __repr__(self):
        return(str(self.label))

    def __hash__(self):
        return hash(self.label)

    def __eq__(self, other):
        return self.label == other.label


def json_dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__


class Simulation(object):
    c_distance = 15  # An arbitrary parameter to determine which patches are connected

    def __init__(self, seed, nr_patches):
        self.civs = [{'color': 'r'}, {'color': 'b'}, {'color': 'y'}]
        self.step = 0
        self.patches = []
        self.history = []
        self.nr_patches = nr_patches
        
        if(self.nr_patches > 300):
            self.nr_patches = 300
        
        np.random.seed(seed)

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

    def get_json(self):
        data = json_graph.node_link_data(self.graph)
        data['groups'] = [patch.status for patch in self.graph.nodes()]
        
        return json.dumps(data, default=json_dumper)

