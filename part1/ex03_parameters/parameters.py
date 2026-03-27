"""
Solver parameters.

(a) solve_with_params — apply parameter settings and solve
(b) load_and_solve    — read a model from file, configure, and solve
"""

from pyscipopt import Model


def solve_with_params(model, params):
    """Apply SCIP parameters, solve, and return results.

    Args:
        model:  A pre-built (unsolved) Model.
        params: Dict mapping parameter names to values, e.g.
                {"limits/time": 60, "limits/gap": 0.01}

    Returns:
        dict with keys: "status", "objective", "gap", "n_nodes", "time"

    Use: model.setParam(name, value), getNSols() to check before getObjVal()
    """
    # EXERCISE 3a: Apply parameters and solve

    raise NotImplementedError("Exercise 3a: Apply parameters and solve.")


def load_and_solve(filepath, params=None):
    """Load a model from an MPS/LP file, apply parameters, and solve.

    Returns:
        Same dict as solve_with_params.

    Use: Model(), readProblem(filepath), then call solve_with_params()
    """
    # EXERCISE 3b: Load from file and solve

    model = Model()
    model.readProblem(filepath)
    return solve_with_params(model, params or {})
