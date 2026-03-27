"""
Solving a model and inspecting solutions.

Optimize a model and extract: status, objective, variable values, nodes, time.
"""

from pyscipopt import Model


def solve_and_report(model):
    """Optimize the given model and return solution statistics.

    Steps:
        1. Solve:                model.optimize()
        2. Build a variables dict mapping each variable's name to its value:
              {var.name: model.getVal(var) for var in model.getVars()}
        3. Return a dict with exactly these keys:
              {
                  "status":    model.getStatus(),        # str, e.g. "optimal"
                  "objective": model.getObjVal(),         # float
                  "variables": <the dict from step 2>,    # dict[str, float]
                  "n_nodes":   model.getNNodes(),         # int
                  "time":      model.getSolvingTime(),    # float (seconds)
              }
    """
    # EXERCISE 2: Solve and collect results

    raise NotImplementedError("Exercise 2: Solve the model and return statistics.")
