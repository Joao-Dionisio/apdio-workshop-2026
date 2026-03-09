"""Solution for Exercise 3: Transportation Problem."""

from pyscipopt import Model, quicksum


def transportation(supply, demand, costs):
    m = len(supply)
    n = len(demand)

    model = Model("Transportation")

    x = {}
    for i in range(m):
        for j in range(n):
            x[i, j] = model.addVar(name=f"x_{i}_{j}", vtype="C", lb=0,
                                   obj=costs[i][j])

    for i in range(m):
        model.addCons(quicksum(x[i, j] for j in range(n)) <= supply[i])

    for j in range(n):
        model.addCons(quicksum(x[i, j] for i in range(m)) >= demand[j])

    return model, x
