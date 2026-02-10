"""Solution for Exercise 6: 0-1 Knapsack."""

from pyscipopt import Model, quicksum


def knapsack(weights, values, capacity):
    n = len(weights)

    model = Model("Knapsack")

    x = {}
    for i in range(n):
        x[i] = model.addVar(name=f"x_{i}", vtype="B", obj=values[i])

    model.addCons(quicksum(weights[i] * x[i] for i in range(n)) <= capacity)

    model.setMaximize()

    return model, x
