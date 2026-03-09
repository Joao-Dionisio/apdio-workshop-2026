"""
Graph coloring problem.

Exercise 8: Build a graph coloring IP.

Given an undirected graph, assign a color to each node such that no two
adjacent nodes share the same color, using the minimum number of colors.

Variables:
    x[v, k] in {0, 1} — 1 if node v gets color k
    w[k]    in {0, 1} — 1 if color k is used

Formulation:
    min  sum_k w_k
    s.t. sum_k x[v, k] = 1               for all nodes v    (one color)
         x[u, k] + x[v, k] <= w[k]       for all edges (u,v), colors k
         x[v, k] in {0, 1}
         w[k] in {0, 1}
"""

from pyscipopt import Model, quicksum


def graph_coloring(n_nodes, edges, max_colors):
    """
    Build and return a graph coloring IP.

    Args:
        n_nodes: Number of nodes.
        edges: List of (u, v) tuples representing edges (u < v).
        max_colors: Upper bound on the number of colors.

    Returns:
        model: A PySCIPOpt Model (not yet optimized).
        x: Dict mapping (v, k) to binary variable (node v gets color k).
        w: Dict mapping color k to binary variable (color k is used).
    """
    # =========================================================================
    # EXERCISE 8: Build a graph coloring IP
    # =========================================================================
    #
    # Step 1: Create a Model
    #
    # Step 2: Add binary variables w[k] for each color k with obj=1
    #
    # Step 3: Add binary variables x[v, k] for each node v and color k
    #
    # Step 4: Each node gets exactly one color:
    #         sum_k x[v, k] == 1   for all v
    #
    # Step 5: Conflict constraints — adjacent nodes can't share a color:
    #         x[u, k] + x[v, k] <= w[k]   for all (u,v) in edges, all k
    #
    #         Note: using w[k] instead of 1 on the right-hand side links
    #         the conflict constraints to color usage.
    #
    # Step 6: (Optional) Symmetry breaking — order colors:
    #         w[k] >= w[k+1]   for all k
    #
    # Step 7: Return model, x, w
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 8: Build a graph coloring IP.\n"
        "Hint: Binary x[v,k] for assignment, w[k] for color usage,\n"
        "conflict constraints x[u,k] + x[v,k] <= w[k]."
    )
