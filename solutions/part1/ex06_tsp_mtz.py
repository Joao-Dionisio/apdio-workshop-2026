"""Solution for Exercise 6: TSP with MTZ formulation."""

from pyscipopt import Model, quicksum


def tsp_mtz(distances):
    n = len(distances)
    model = Model("tsp_mtz")

    # Binary edge variables x[i,j] for i != j
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i, j] = model.addVar(vtype="B", obj=distances[i][j],
                                        name=f"x_{i}_{j}")

    # Position variables u[i] for i = 1..n-1
    u = {}
    for i in range(1, n):
        u[i] = model.addVar(vtype="C", lb=1, ub=n - 1, name=f"u_{i}")

    # Out-degree: each city is left exactly once
    for i in range(n):
        model.addCons(quicksum(x[i, j] for j in range(n) if j != i) == 1)

    # In-degree: each city is entered exactly once
    for j in range(n):
        model.addCons(quicksum(x[i, j] for i in range(n) if i != j) == 1)

    # MTZ subtour elimination (only non-depot cities)
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                model.addCons(u[i] - u[j] + n * x[i, j] <= n - 1)

    return model, x
