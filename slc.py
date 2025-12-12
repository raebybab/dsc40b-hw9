def slc(graph, d, k):
    """
    Perform single-linkage clustering using Kruskal’s algorithm.

    Parameters
    ----------
    graph : dsc40graph.UndirectedGraph
        The input graph.
    d : function
        A distance function taking an (u, v) tuple and returning a weight.
    k : int
        The desired number of clusters.

    Returns
    -------
    frozenset of frozensets
        Each frozenset is a cluster of nodes.
    """

    # Step 1 — all vertices
    nodes = list(graph.nodes)

    # Create DSF structure for all nodes
    dsf = DisjointSetForest(nodes)

    # Step 2 — build a list of all edges with distances
    edges = []
    for u, v in graph.edges:
        dist = d((u, v))
        edges.append((dist, u, v))

    # Step 3 — sort edges by distance
    edges.sort(key=lambda x: x[0])

    # Number of clusters starts as n (each node isolated)
    num_clusters = len(nodes)

    # Step 4 — Kruskal but stop once we reach k clusters
    for dist, u, v in edges:
        if num_clusters == k:
            break

        # If u and v are in different clusters, union them
        if not dsf.in_same_set(u, v):
            dsf.union(u, v)
            num_clusters -= 1

    # Step 5 — extract clusters
    clusters = {}

    for node in nodes:
        root = dsf.find_set(node)
        clusters.setdefault(root, set()).add(node)

    # Convert to frozenset of frozensets (required output format)
    result = frozenset(frozenset(cluster) for cluster in clusters.values())

    return result