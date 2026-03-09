"""Solution for Exercise 4: Portfolio Optimization."""

from pyscipopt import Model, quicksum


def portfolio(expected_returns, covariance, r_min):
    n = len(expected_returns)

    model = Model("Portfolio")

    x = {}
    for i in range(n):
        x[i] = model.addVar(name=f"x_{i}", vtype="C", lb=0, ub=1)

    # Auxiliary variable for the objective (portfolio variance)
    t = model.addVar(name="variance", vtype="C", lb=0, obj=1)

    # Budget constraint
    model.addCons(quicksum(x[i] for i in range(n)) == 1)

    # Return constraint
    model.addCons(
        quicksum(expected_returns[i] * x[i] for i in range(n)) >= r_min
    )

    # Quadratic constraint: t >= x^T Sigma x
    model.addCons(
        t >= quicksum(covariance[i][j] * x[i] * x[j]
                      for i in range(n) for j in range(n))
    )

    return model, x
