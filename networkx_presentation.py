class Simulation(object):
    nr_patches = 100   # Number of patches
    c_distance = 15  # An arbitrary parameter to determine which patches are connected

    def __init__(self):
        self.civs = [{'color': 'r'}, {'color': 'b'}, {'color': 'y'}]
        self.step = 0
        self.patches = []

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

    def draw_graph(self):
        pylab.figure(1, figsize=(8, 8))
        nx.draw(self.graph, {patch: patch.pos for patch in self.graph.nodes()},
                with_labels=True,
                node_color=[patch.status for patch in self.graph.nodes()])
        pylab.show()
