from disjoint_set_forest import DisjointSetForest

def slc(graph, d, k):
    nodes = list(graph.nodes)
    dsf = DisjointSetForest(nodes)

    edges = []
    for u, v in graph.edges:
        edges.append((d((u, v)), u, v))

    edges.sort(key=lambda x: x[0])

    num_clusters = len(nodes)

    for dist, u, v in edges:
        if num_clusters == k:
            break

        if not dsf.in_same_set(u, v):
            dsf.union(u, v)
            num_clusters -= 1

    clusters = {}
    for node in nodes:
        root = dsf.find_set(node)
        clusters.setdefault(root, set()).add(node)

    return frozenset(frozenset(cluster) for cluster in clusters.values())