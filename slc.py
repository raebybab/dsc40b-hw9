class DisjointSetForest:
    def __init__(self, elements):
        self._core = _DisjointSetForestCore()
        self.element_to_id = {}
        self.id_to_element = {}

        for element in elements:
            eid = self._core.make_set()
            self.element_to_id[element] = eid
            self.id_to_element[eid] = element

    def find_set(self, element):
        """Return the representative of the set containing element."""
        return self.id_to_element[
            self._core.find_set(self.element_to_id[element])
        ]

    def union(self, x, y):
        """Union the sets containing x and y."""
        x_id = self.element_to_id[x]
        y_id = self.element_to_id[y]
        self._core.union(x_id, y_id)

    def in_same_set(self, x, y):
        """Return True if x and y belong to the same set."""
        return self.find_set(x) == self.find_set(y)


class _DisjointSetForestCore:
    def __init__(self):
        self._parent = []
        self._rank = []
        self._size_of_set = []

    def make_set(self):
        """Create a new singleton set, return its id."""
        x = len(self._parent)
        self._parent.append(None)
        self._rank.append(0)
        self._size_of_set.append(1)
        return x

    def find_set(self, x):
        """Path compression find."""
        parent = self._parent[x]
        if parent is None:
            return x
        root = self.find_set(parent)
        self._parent[x] = root
        return root

    def union(self, x, y):
        """Union by rank."""
        x_rep = self.find_set(x)
        y_rep = self.find_set(y)

        if x_rep == y_rep:
            return

        if self._rank[x_rep] > self._rank[y_rep]:
            self._parent[y_rep] = x_rep
            self._size_of_set[x_rep] += self._size_of_set[y_rep]
        else:
            self._parent[x_rep] = y_rep
            self._size_of_set[y_rep] += self._size_of_set[x_rep]
            if self._rank[x_rep] == self._rank[y_rep]:
                self._rank[y_rep] += 1


# ================================
# Single Linkage Clustering (Kruskal-based)
# ================================

def slc(graph, d, k):
    nodes = list(graph.nodes)
    dsf = DisjointSetForest(nodes)
    num_clusters = len(nodes)

    weighted_edges = []
    for u, v in graph.edges:
        weighted_edges.append((d((u, v)), u, v))

    weighted_edges.sort(key=lambda x: x[0])

    for weight, u, v in weighted_edges:
        if num_clusters == k:
            break
        if not dsf.in_same_set(u, v):
            dsf.union(u, v)
            num_clusters -= 1

    clusters = {}
    for node in nodes:
        rep = dsf.find_set(node)
        if rep not in clusters:
            clusters[rep] = set()
        clusters[rep].add(node)

    return frozenset(frozenset(cluster) for cluster in clusters.values())