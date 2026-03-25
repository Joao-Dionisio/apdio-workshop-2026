"""
Graph coloring problem.

    min  sum_k w_k
    s.t. sum_k x[v, k] = 1               for all nodes v
         x[u, k] + x[v, k] <= w[k]       for all edges (u,v), colors k
         x[v, k], w[k] in {0, 1}
"""

from pyscipopt import Model, quicksum


def graph_coloring(n_nodes, edges, max_colors):
    """Build and return a graph coloring IP.

    Returns:
        (model, x, w) — model, assignment dict x[(v,k)], usage dict w[k].
    """
    # EXERCISE 7: Build the graph coloring IP

    model = Model("graph_coloring")

    raise NotImplementedError("Exercise 7: Build a graph coloring IP.")
