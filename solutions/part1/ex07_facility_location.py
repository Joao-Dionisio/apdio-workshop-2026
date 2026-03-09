"""Solution for Exercise 7: Uncapacitated Facility Location."""

from pyscipopt import Model, quicksum


def facility_location(fixed_costs, connection_costs):
    m = len(fixed_costs)
    n = len(connection_costs[0])

    model = Model("FacilityLocation")

    y = {}
    for i in range(m):
        y[i] = model.addVar(name=f"y_{i}", vtype="B", obj=fixed_costs[i])

    x = {}
    for i in range(m):
        for j in range(n):
            x[i, j] = model.addVar(name=f"x_{i}_{j}", vtype="C", lb=0, ub=1,
                                   obj=connection_costs[i][j])

    for j in range(n):
        model.addCons(quicksum(x[i, j] for i in range(m)) == 1)

    for i in range(m):
        for j in range(n):
            model.addCons(x[i, j] <= y[i])

    return model, y, x
