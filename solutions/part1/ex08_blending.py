"""Solution for Exercise 8: Nonlinear Blending (Pooling Problem)."""

from pyscipopt import Model, quicksum


def blending(sources, products):
    model = Model("blending")

    S = range(len(sources))
    P = range(len(products))

    # Flow from source s to pool
    x = {s: model.addVar(vtype="C", lb=0, name=f"x_{s}") for s in S}
    # Flow from pool to product p
    y = {p: model.addVar(vtype="C", lb=0, name=f"y_{p}") for p in P}
    # Direct bypass from source s to product p
    z = {(s, p): model.addVar(vtype="C", lb=0, name=f"z_{s}_{p}")
         for s in S for p in P}
    # Pool quality
    l = model.addVar(vtype="C", lb=0, name="lambda")
    # Product demand (total delivery)
    d = {p: model.addVar(vtype="C", lb=0, name=f"d_{p}") for p in P}

    # Objective: maximize revenue - cost
    revenue = quicksum(products[p]["revenue"] * d[p] for p in P)
    cost = quicksum(sources[s]["cost"] * (x[s] + quicksum(z[s, p] for p in P))
                    for s in S)
    model.setObjective(revenue - cost, "maximize")

    # Pool balance: sum of inflows = sum of outflows
    model.addCons(quicksum(x[s] for s in S) == quicksum(y[p] for p in P))

    # Pool quality definition (bilinear): lambda * sum(x_s) = sum(q_s * x_s)
    model.addCons(
        l * quicksum(x[s] for s in S) ==
        quicksum(sources[s]["quality"] * x[s] for s in S)
    )

    # Product quality constraints (bilinear)
    for p in P:
        model.addCons(
            l * y[p] + quicksum(sources[s]["quality"] * z[s, p] for s in S)
            <= products[p]["max_quality"] * d[p]
        )

    # Product demand definitions
    for p in P:
        model.addCons(d[p] == y[p] + quicksum(z[s, p] for s in S))

    return model, x, y, z, l
