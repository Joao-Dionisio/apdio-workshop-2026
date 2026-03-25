"""
Subtour detection for the TSP.

Given a set of selected edges and the number of nodes,
find all connected components. If there's more than one,
each represents a subtour that violates an SEC.
"""


def find_subtours(selected_edges, n_nodes):
    """
    Find subtours (connected components) in a graph defined by selected edges.

    Args:
        selected_edges: List of (i, j) tuples (undirected).
        n_nodes: Total number of nodes.

    Returns:
        List of sets (one per component), or [] if a single valid tour.

    Example:
        >>> find_subtours([(0,1), (1,2), (2,0), (3,4), (4,5), (5,3)], 6)
        [{0, 1, 2}, {3, 4, 5}]
        >>> find_subtours([(0,1), (1,2), (2,3), (3,0)], 4)
        []
    """
    # EXERCISE 1: Implement subtour detection
    #
    # Hint: Build an adjacency list, then use DFS/BFS to find components.
    # Or use networkx: networkx.connected_components(networkx.Graph(selected_edges))

    import networkx as nx
    G = nx.Graph()
    G.add_nodes_from(range(n_nodes))
    G.add_edges_from(selected_edges)
    components = list(nx.connected_components(G))

    return components if len(components) > 1 else []
