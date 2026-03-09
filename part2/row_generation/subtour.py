"""
Subtour detection for the TSP.

Exercise 1: Implement the find_subtours function.

A subtour is a cycle that visits only a subset of cities. In a valid
TSP solution, there should be exactly one tour visiting all cities.
Subtours correspond to violated Subtour Elimination Constraints (SECs).

Your task: Given a set of selected edges and the number of nodes,
find all connected components. If there's more than one component,
each represents a subtour that needs to be eliminated.
"""


def find_subtours(selected_edges, n_nodes):
    """
    Find subtours (connected components) in a graph defined by selected edges.

    In a valid TSP solution, all nodes should be in a single connected
    component forming a Hamiltonian cycle. If the graph has multiple
    connected components, each component represents a subtour that
    violates the subtour elimination constraints.

    Args:
        selected_edges: List of (i, j) tuples representing selected edges.
                       Edges are undirected (symmetric TSP).
        n_nodes: Total number of nodes in the graph.

    Returns:
        List of sets, where each set contains the nodes in a subtour.
        Returns an empty list [] if all nodes are in a single connected
        component (valid tour).

    Example:
        >>> find_subtours([(0,1), (1,2), (2,0), (3,4), (4,5), (5,3)], 6)
        [{0, 1, 2}, {3, 4, 5}]  # Two triangular subtours

        >>> find_subtours([(0,1), (1,2), (2,3), (3,0)], 4)
        []  # Single tour through all 4 nodes
    """
    # =========================================================================
    # EXERCISE 1: Implement subtour detection
    # =========================================================================
    #
    # Hint 1: Build an adjacency list from selected_edges.
    #         Remember edges are undirected: (i,j) means both i-j and j-i.
    #
    # Hint 2: Use DFS or BFS to find connected components:
    #         - Start from an unvisited node
    #         - Visit all reachable nodes, marking them as visited
    #         - Repeat until all nodes are visited
    #
    # Hint 3: Alternative approach using Union-Find:
    #         - Initialize each node as its own parent
    #         - For each edge (i,j), union the sets containing i and j
    #         - Nodes with the same root are in the same component
    #
    # Return: List of sets (components). If only one component with all
    #         n_nodes, return empty list [].
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 1: Implement subtour detection using DFS or Union-Find.\n"
        "Hint: Build an adjacency list from edges, then find connected components.\n"
        "If there's only one component containing all nodes, return []."
    )
