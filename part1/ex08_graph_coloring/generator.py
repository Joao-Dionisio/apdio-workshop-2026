"""
Random graph coloring instance generator.
"""

import random


def random_graph_coloring_instance(n_nodes, edge_prob=0.3, seed=0):
    """
    Generate a random graph for coloring (Erdos-Renyi model).

    Args:
        n_nodes: Number of nodes.
        edge_prob: Probability that each edge exists.
        seed: Random seed for reproducibility.

    Returns:
        n_nodes: Number of nodes.
        edges: List of (i, j) tuples with i < j.
    """
    random.seed(seed)

    edges = []
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if random.random() < edge_prob:
                edges.append((i, j))

    return n_nodes, edges


def petersen_graph():
    """
    Return the Petersen graph (10 nodes, 15 edges, chromatic number = 3).

    Returns:
        n_nodes: 10
        edges: List of 15 edges.
    """
    edges = [
        # Outer cycle
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
        # Inner pentagram
        (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
        # Spokes
        (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
    ]
    return 10, edges


if __name__ == "__main__":
    n, edges = petersen_graph()
    print(f"Petersen graph: {n} nodes, {len(edges)} edges")
    print(f"Edges: {edges}")

    n, edges = random_graph_coloring_instance(8, seed=42)
    print(f"\nRandom graph: {n} nodes, {len(edges)} edges")
