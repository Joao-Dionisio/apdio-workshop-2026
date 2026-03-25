"""
Solving a model and inspecting solutions.

Optimize a model and extract: status, objective, variable values, nodes, time.
"""

from pyscipopt import Model


def solve_and_report(model):
    """Optimize the given model and return solution statistics.

    Returns:
        dict with keys: "status", "objective", "variables", "n_nodes", "time"

    Use: model.optimize(), getStatus(), getObjVal(), getVars(), getVal(),
         getNNodes(), getSolvingTime()
    """
    # EXERCISE 2: Solve and collect results

    raise NotImplementedError("Exercise 2: Solve the model and return statistics.")
