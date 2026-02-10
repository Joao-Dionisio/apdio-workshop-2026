"""Solution for Exercise 4: Blending Problem."""

from pyscipopt import Model, quicksum


def blending(costs, availability, qualities, quality_lb, quality_ub,
             total_production):
    m = len(costs)
    p = len(quality_lb)

    model = Model("Blending")

    x = {}
    for i in range(m):
        x[i] = model.addVar(name=f"x_{i}", vtype="C", lb=0,
                            ub=availability[i], obj=costs[i])

    model.addCons(quicksum(x[i] for i in range(m)) == total_production)

    for q in range(p):
        model.addCons(
            quicksum(qualities[i][q] * x[i] for i in range(m))
            >= quality_lb[q] * total_production
        )
        model.addCons(
            quicksum(qualities[i][q] * x[i] for i in range(m))
            <= quality_ub[q] * total_production
        )

    model.setMinimize()

    return model, x
