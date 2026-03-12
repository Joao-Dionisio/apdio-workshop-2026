"""
Compact MTZ formulation for the Traveling Salesman Problem.

This is the reference solution used in Part 2 for comparison against
row generation. The exercise stub is in part1/ex11_tsp_mtz/.
"""

from pyscipopt import Model, quicksum


def tsp_mtz(distances):
    """
    Solve TSP using the Miller-Tucker-Zemlin compact formulation.

    Args:
        distances: n x n symmetric distance matrix

    Returns:
        model: PySCIPOpt Model object
        x: dict mapping (i,j) to binary edge variables
    """
    n = len(distances)
    model = Model("TSP-MTZ")

    # Binary edge variables
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i, j] = model.addVar(vtype="B", obj=distances[i][j],
                                        name=f"x_{i}_{j}")

    # Position variables (u[0] is implicitly 0)
    u = {}
    for i in range(1, n):
        u[i] = model.addVar(vtype="C", lb=1, ub=n - 1, name=f"u_{i}")

    # Out-degree: leave each city exactly once
    for i in range(n):
        model.addCons(quicksum(x[i, j] for j in range(n) if j != i) == 1)

    # In-degree: enter each city exactly once
    for j in range(n):
        model.addCons(quicksum(x[i, j] for i in range(n) if i != j) == 1)

    # MTZ subtour elimination
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                model.addCons(u[i] - u[j] + n * x[i, j] <= n - 1)

    return model, x
