"""Solution for Exercise 8: Graph Coloring."""

from pyscipopt import Model, quicksum


def graph_coloring(n_nodes, edges, max_colors):
    model = Model("GraphColoring")

    w = {}
    for k in range(max_colors):
        w[k] = model.addVar(name=f"w_{k}", vtype="B", obj=1)

    x = {}
    for v in range(n_nodes):
        for k in range(max_colors):
            x[v, k] = model.addVar(name=f"x_{v}_{k}", vtype="B")

    for v in range(n_nodes):
        model.addCons(quicksum(x[v, k] for k in range(max_colors)) == 1)

    for u, v in edges:
        for k in range(max_colors):
            model.addCons(x[u, k] + x[v, k] <= w[k])

    for k in range(max_colors - 1):
        model.addCons(w[k] >= w[k + 1])

    model.setMinimize()

    return model, x, w
