"""Solution for Exercise 2: Solving and Inspecting Solutions."""

from pyscipopt import Model


def solve_and_report(model):
    model.optimize()

    return {
        "status": model.getStatus(),
        "objective": model.getObjVal(),
        "variables": {var.name: model.getVal(var) for var in model.getVars()},
        "n_nodes": model.getNNodes(),
        "time": model.getSolvingTime(),
    }
