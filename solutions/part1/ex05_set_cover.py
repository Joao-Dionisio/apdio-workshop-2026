"""Solution for Exercise 5: Set Cover."""

from pyscipopt import Model, quicksum


def set_cover(universe, subsets, costs):
    model = Model("SetCover")

    y = {}
    for j in range(len(subsets)):
        y[j] = model.addVar(name=f"y_{j}", vtype="B", obj=costs[j])

    for e in universe:
        model.addCons(
            quicksum(y[j] for j in range(len(subsets)) if e in subsets[j]) >= 1
        )

    return model, y
