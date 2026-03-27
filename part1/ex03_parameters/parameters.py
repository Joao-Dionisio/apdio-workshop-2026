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

    Steps:
        1. Apply each parameter:  for name, val in params.items():
                                      model.setParam(name, val)
        2. Solve:                 model.optimize()
        3. CAREFUL: calling model.getObjVal() when the model is infeasible
           (or no solution was found) will crash. Check first:
              if model.getNSols() > 0:  objective = model.getObjVal()
              else:                     objective = None
        4. Return a dict:
              {
                  "status":    model.getStatus(),        # str
                  "objective": <from step 3>,             # float or None
                  "gap":       model.getGap(),            # float
                  "n_nodes":   model.getNNodes(),         # int
                  "time":      model.getSolvingTime(),    # float (seconds)
              }
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
