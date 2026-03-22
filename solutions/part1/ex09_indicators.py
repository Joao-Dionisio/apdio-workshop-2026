"""Solution for Exercise 9: Indicator Constraints."""

from pyscipopt import Model, quicksum


def generator_scheduling_bigm(demand, fixed_costs, var_costs, p_min, p_max):
    n = len(fixed_costs)
    model = Model("generator_bigm")

    y = {i: model.addVar(vtype="B", name=f"y_{i}") for i in range(n)}
    p = {i: model.addVar(vtype="C", lb=0, name=f"p_{i}") for i in range(n)}

    model.setObjective(
        quicksum(fixed_costs[i] * y[i] + var_costs[i] * p[i] for i in range(n)),
        "minimize"
    )

    # Demand constraint
    model.addCons(quicksum(p[i] for i in range(n)) >= demand)

    for i in range(n):
        # Upper bound: p[i] <= p_max[i] * y[i]
        model.addCons(p[i] <= p_max[i] * y[i])
        # Lower bound (big-M): p[i] >= p_min[i] * y[i]
        model.addCons(p[i] >= p_min[i] * y[i])

    return model, y, p


def generator_scheduling_indicator(demand, fixed_costs, var_costs, p_min, p_max):
    n = len(fixed_costs)
    model = Model("generator_indicator")

    y = {i: model.addVar(vtype="B", name=f"y_{i}") for i in range(n)}
    p = {i: model.addVar(vtype="C", lb=0, name=f"p_{i}") for i in range(n)}

    model.setObjective(
        quicksum(fixed_costs[i] * y[i] + var_costs[i] * p[i] for i in range(n)),
        "minimize"
    )

    # Demand constraint
    model.addCons(quicksum(p[i] for i in range(n)) >= demand)

    for i in range(n):
        # Upper bound: p[i] <= p_max[i] * y[i]
        model.addCons(p[i] <= p_max[i] * y[i])
        # Indicator: y[i] = 1 => p[i] >= p_min[i]
        model.addConsIndicator(p[i] >= p_min[i], y[i])

    return model, y, p
