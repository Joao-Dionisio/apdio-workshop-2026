"""Solution for Exercise 3: Solver parameters."""

from pyscipopt import Model


def solve_with_params(model, params):
    model.hideOutput()
    for name, value in params.items():
        model.setParam(name, value)

    model.optimize()

    objective = None
    if model.getNSols() > 0:
        objective = model.getObjVal()

    return {
        "status": model.getStatus(),
        "objective": objective,
        "gap": model.getGap(),
        "n_nodes": model.getNNodes(),
        "time": model.getSolvingTime(),
    }


def load_and_solve(filepath, params=None):
    model = Model()
    model.readProblem(filepath)
    return solve_with_params(model, params or {})
