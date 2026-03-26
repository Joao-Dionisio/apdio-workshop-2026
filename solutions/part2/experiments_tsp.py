"""Solution for Exercise 3: TSP computational experiments."""

from time import time

from generator import random_euclidean_tsp
from compact_mtz import tsp_mtz
from tsp import tsp_rowgen


def lp_bound(build_fn, distances):
    model, x = build_fn(distances)
    for v in model.getVars():
        if v.vtype() != 'CONTINUOUS':
            model.chgVarType(v, 'CONTINUOUS')
    model.hideOutput()
    model.optimize()
    return model.getObjVal()


def solve_and_collect(build_fn, distances, time_limit=30):
    model, x = build_fn(distances)
    model.hideOutput()
    model.setParam("limits/time", time_limit)

    model.optimize()

    return {
        "obj": model.getObjVal() if model.getStatus() == "optimal" else None,
        "time": model.getSolvingTime(),
        "nodes": model.getNNodes(),
        "status": model.getStatus(),
    }
