"""
Subtour detection for the TSP.

Given a set of selected edges and the number of nodes,
find all connected components. If there's more than one,
each represents a subtour that violates an SEC.
"""

from collections import defaultdict


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
    adj = defaultdict(set)
    for i, j in selected_edges:
        adj[i].add(j)
        adj[j].add(i)

    visited = set()
    components = []

    for node in range(n_nodes):
        if node in visited:
            continue
        component = set()
        stack = [node]
        while stack:
            v = stack.pop()
            if v in visited:
                continue
            visited.add(v)
            component.add(v)
            for neighbor in adj[v]:
                if neighbor not in visited:
                    stack.append(neighbor)
        components.append(component)

    if len(components) == 1:
        return []
    return components
