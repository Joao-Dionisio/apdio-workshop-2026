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
    """Build and return a graph coloring IP."""
    # =========================================================================
    # EXERCISE 10: Build a graph coloring IP
    # =========================================================================
    #
    # Think about what prevents adjacent nodes from sharing a color,
    # and how to track which colors are actually used.
    #
    # Return model, x, w
    #
    # =========================================================================

    raise NotImplementedError("Exercise 10: Build a graph coloring IP.")
