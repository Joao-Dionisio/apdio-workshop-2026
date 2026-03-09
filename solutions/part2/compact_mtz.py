"""Solution for Exercise 0: Compact MTZ formulation for TSP."""

from pyscipopt import Model, quicksum


def tsp_mtz(distances):
    model = Model("TSP-MTZ")
    n = len(distances)

    # Binary edge variables (directed formulation for MTZ)
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i, j] = model.addVar(vtype="B", obj=distances[i][j],
                                       name=f"x_{i}_{j}")

    # Position variables (continuous)
    u = {}
    for i in range(1, n):  # u[0] is fixed implicitly
        u[i] = model.addVar(vtype="C", lb=1, ub=n - 1, name=f"u_{i}")

    # Each city must be left exactly once
    for i in range(n):
        model.addCons(
            quicksum(x[i, j] for j in range(n) if j != i) == 1,
            name=f"out_{i}"
        )

    # Each city must be entered exactly once
    for j in range(n):
        model.addCons(
            quicksum(x[i, j] for i in range(n) if i != j) == 1,
            name=f"in_{j}"
        )

    # MTZ subtour elimination constraints
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                model.addCons(
                    u[i] - u[j] + n * x[i, j] <= n - 1,
                    name=f"mtz_{i}_{j}"
                )

    return model, x
